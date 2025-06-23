import streamlit as st
import requests
import json
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"

def make_api_request(endpoint: str, data: Dict[Any, Any] = None) -> Dict[Any, Any]:
    """Make API request to FastAPI backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if data:
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API. Make sure FastAPI server is running on localhost:8000"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}

def main():
    st.set_page_config(
        page_title="Email Automation Agent",
        page_icon="📧",
        layout="wide"
    )
    
    st.title("📧 Email Automation Agent")
    st.markdown("Send automated shortlisting emails to candidates with optional test links")
    
    # Sidebar for API status
    with st.sidebar:
        st.header("🔧 API Status")
        if st.button("Check API Health"):
            health_response = make_api_request("/health")
            if "error" in health_response:
                st.error(f"❌ API Offline: {health_response['error']}")
            else:
                st.success("✅ API Online")
        
        st.markdown("---")
        st.markdown("**API Endpoints:**")
        st.code("http://localhost:8000")
        st.markdown("Make sure FastAPI server is running!")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📨 Single Email with Test", "📬 Bulk Emails", "📊 API Info"])
    
    with tab1:
        st.header("Send Email with Test Link")
        st.markdown("Send a personalized shortlisting email to a single candidate with an assessment link.")
        
        with st.form("single_email_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                candidate_name = st.text_input(
                    "Candidate Name",
                    placeholder="e.g., John Doe",
                    help="Name of the candidate to personalize the email"
                )
                
                email_address = st.text_input(
                    "Email Address",
                    placeholder="candidate@example.com",
                    help="Email address of the candidate"
                )
            
            with col2:
                test_link = st.text_input(
                    "Test/Assessment Link",
                    placeholder="https://assessment-platform.com/test/123",
                    help="URL for the assessment or test"
                )
            
            # Preview section
            if candidate_name and email_address and test_link:
                with st.expander("📋 Email Preview"):
                    st.markdown(f"**To:** {email_address}")
                    st.markdown(f"**Subject:** 🎉 Application Update - You're Shortlisted!")
                    st.markdown(f"**Candidate:** {candidate_name}")
                    st.markdown(f"**Test Link:** {test_link}")
            
            submit_single = st.form_submit_button("📤 Send Email", type="primary")
            
            if submit_single:
                if not all([candidate_name, email_address, test_link]):
                    st.error("❌ Please fill in all fields")
                elif "@" not in email_address:
                    st.error("❌ Please enter a valid email address")
                elif not test_link.startswith("http"):
                    st.error("❌ Please enter a valid URL for the test link")
                else:
                    with st.spinner("Sending email..."):
                        data = {
                            "email_input": email_address,
                            "test_link": test_link,
                            "candidate_name": candidate_name
                        }
                        
                        response = make_api_request("/send-email-with-test-link", data)
                        
                        if "error" in response:
                            st.error(f"❌ {response['error']}")
                        elif response.get("success"):
                            st.success(f"✅ {response['message']}")
                            st.balloons()
                        else:
                            st.error(f"❌ {response.get('message', 'Unknown error')}")
    
    with tab2:
        st.header("Send Bulk Emails")
        st.markdown("Send shortlisting emails to multiple candidates (without test links).")
        
        with st.form("bulk_email_form"):
            st.markdown("**Enter email addresses (one per line or comma-separated):**")
            email_input = st.text_area(
                "Email Addresses",
                placeholder="candidate1@example.com\ncandidate2@example.com\ncandidate3@example.com",
                height=150,
                help="Enter multiple email addresses separated by new lines or commas"
            )
            
            # Email count preview
            if email_input:
                emails = []
                for email in email_input.replace(',', '\n').split('\n'):
                    email = email.strip()
                    if email and '@' in email:
                        emails.append(email)
                
                if emails:
                    st.info(f"📊 Found {len(emails)} valid email address(es)")
                    with st.expander("📋 Email List Preview"):
                        for i, email in enumerate(emails, 1):
                            st.write(f"{i}. {email}")
                else:
                    st.warning("⚠️ No valid email addresses found")
            
            submit_bulk = st.form_submit_button("📤 Send Bulk Emails", type="primary")
            
            if submit_bulk:
                if not email_input.strip():
                    st.error("❌ Please enter at least one email address")
                else:
                    emails = []
                    for email in email_input.replace(',', '\n').split('\n'):
                        email = email.strip()
                        if email and '@' in email:
                            emails.append(email)
                    
                    if not emails:
                        st.error("❌ No valid email addresses found")
                    else:
                        with st.spinner(f"Sending emails to {len(emails)} recipients..."):
                            # Note: The bulk endpoint is commented out in main.py
                            # For now, we'll show a message about this
                            st.warning("⚠️ Bulk email endpoint is currently disabled in the API. Please enable it in main.py or send emails individually.")
                            
                            # If bulk endpoint were enabled, the code would be:
                            # data = {"email_input": email_input}
                            # response = make_api_request("/send-bulk-emails", data)
    
    with tab3:
        st.header("API Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📡 API Details")
            api_info = make_api_request("/")
            
            if "error" in api_info:
                st.error(f"❌ Cannot reach API: {api_info['error']}")
            else:
                st.json(api_info)
        
        with col2:
            st.subheader("🏥 Health Check")
            if st.button("Run Health Check"):
                health_response = make_api_request("/health")
                if "error" in health_response:
                    st.error(f"❌ {health_response['error']}")
                else:
                    st.success("✅ API is healthy")
                    st.json(health_response)
        
        st.subheader("📖 Usage Instructions")
        st.markdown("""
        1. **Start the FastAPI server:**
           ```bash
           uvicorn main:app --host 0.0.0.0 --port 8000
           ```
        
        2. **Configure environment variables** in `.env`:
           - `SENDER_EMAIL`: Your Outlook email
           - `APP_PASSWORD`: Your app password
           - `GEMINI_API_KEY`: Your Gemini API key
        
        3. **Use the tabs above** to send emails:
           - **Single Email with Test**: For sending personalized emails with assessment links
           - **Bulk Emails**: For sending multiple emails at once (when enabled)
        
        4. **Check API status** in the sidebar before sending emails
        """)
        
        st.subheader("🔗 Useful Links")
        st.markdown("""
        - [FastAPI Docs](http://localhost:8000/docs) (when server is running)
        - [API Health Check](http://localhost:8000/health)
        - [GitHub Repository](https://github.com) (add your repo link)
        """)

if __name__ == "__main__":
    main()
