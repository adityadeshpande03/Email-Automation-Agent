import os
from agno.agent import Agent
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.utils.pprint import pprint_run_response
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.smtp_connection import send_outlook_email

load_dotenv()

def process_email_with_test_link(email_input: str = "", test_link: str = "", candidate_name: str = "Candidate"):
    """Send email with test link to candidate"""
    # Validate inputs
    if not email_input:
        return "Please provide an email address."
    
    if not test_link:
        return "Please provide a test link."
    
    # Clean and validate email
    email = email_input.strip()
    if '@' not in email:
        return "Please provide a valid email address."
    
    print(f"Sending email to: {email}")
    print(f"Test link: {test_link}")
    print(f"Candidate name: {candidate_name}")
    
    # Get sender credentials from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("APP_PASSWORD")
    
    if not sender_email or not app_password:
        return "Error: SENDER_EMAIL and APP_PASSWORD must be set in environment variables"
    
    # Prepare recipient data with test link
    recipient_data = [{
        'email': email,
        'test_link': test_link.strip(),
        'name': candidate_name.strip()
    }]
    
    try:
        # Send email using the template with test link
        send_outlook_email(sender_email, app_password, recipient_data)
        return f"Successfully sent shortlisting email with test link to {email}"
    except Exception as e:
        return f"Error sending email: {str(e)}"

def process_email_input(email_input: str = ""):
    """Parse email input and send template emails without test link"""
    # If no email_input provided, return message
    if not email_input:
        return "Please provide email addresses to send notifications to."
    
    # Parse email addresses (comma-separated or space-separated)
    email_list = []
    for email in email_input.replace(',', ' ').split():
        email = email.strip()
        if '@' in email:
            email_list.append(email)
    
    if not email_list:
        return "No valid email addresses found. Please enter valid email addresses."
    
    print(f"Found {len(email_list)} email address(es): {', '.join(email_list)}")
    
    # Get sender credentials from environment variables
    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("APP_PASSWORD")
    
    if not sender_email or not app_password:
        return "Error: SENDER_EMAIL and APP_PASSWORD must be set in environment variables"
    
    # Send emails using the template (without test link for manual input)
    try:
        send_outlook_email(sender_email, app_password, email_list)
        return f"Successfully sent shortlisting emails to {len(email_list)} recipients"
    except Exception as e:
        return f"Error sending emails: {str(e)}"

email_agent = Agent(
    name="Email Automation Agent",
    description="An agent that sends shortlisting email notifications to candidates. Can send emails with or without test links.",
    model=Gemini(
        id="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    ),
    tools=[process_email_with_test_link, process_email_input],
    memory=None,
)

# The agent is now ready to be imported and used by the FastAPI application