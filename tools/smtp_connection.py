import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

def get_html_template(test_link=None, candidate_name="Candidate"):
    """Returns a professional HTML email template with optional test link"""
    
    # Test link section - only show if test_link is provided
    test_link_section = ""
    if test_link:
        test_link_section = f"""
            <div style="background: #e8f5e8; border-left: 4px solid #27ae60; padding: 20px; margin: 25px 0; border-radius: 0 8px 8px 0;">
                <h3 style="color: #2c3e50; margin: 0 0 15px 0; font-size: 18px;">🔗 Assessment Link:</h3>
                <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6;">
                    Please complete the online assessment using the link below:
                </p>
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{test_link}" 
                       style="display: inline-block; background: #3498db; color: white; padding: 15px 30px; 
                              text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px;
                              box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);">
                        🎯 Start Assessment
                    </a>
                </div>
                <p style="margin: 15px 0 0 0; font-size: 14px; color: #7f8c8d; text-align: center;">
                    Click the button above or copy this link: <br>
                    <span style="word-break: break-all; font-family: monospace; background: #f8f9fa; padding: 4px 8px; border-radius: 4px;">
                        {test_link}
                    </span>
                </p>
            </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Application Update</title>
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 300;">🎉 Congratulations!</h1>
            <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 16px;">You've been shortlisted!</p>
        </div>
        
        <div style="background: #ffffff; padding: 40px; border: 1px solid #e0e0e0; border-top: none;">
            <h2 style="color: #2c3e50; margin-bottom: 20px; font-size: 24px;">Dear {candidate_name},</h2>
            
            <p style="margin-bottom: 20px; font-size: 16px; line-height: 1.8;">
                We are <strong style="color: #27ae60;">pleased to inform you</strong> that you have been 
                <span style="background: #f8f9fa; padding: 2px 8px; border-radius: 4px; font-weight: 600; color: #2c3e50;">shortlisted</span> 
                for the next round of our selection process.
            </p>
            
            {test_link_section}
            
            <div style="background: #f8f9fa; border-left: 4px solid #3498db; padding: 20px; margin: 25px 0; border-radius: 0 8px 8px 0;">
                <h3 style="color: #2c3e50; margin: 0 0 10px 0; font-size: 18px;">📋 Next Steps:</h3>
                <p style="margin: 0; font-size: 16px; line-height: 1.6;">
                    {"Complete the assessment above and our" if test_link else "Our"} HR team will contact you within the <strong>next 2-3 days</strong> with detailed instructions 
                    for the upcoming round and guide you through the next steps.
                </p>
            </div>
            
            <p style="margin: 25px 0; font-size: 16px; line-height: 1.8;">
                Thank you for your interest in joining our organization. We look forward to proceeding with your application 
                and getting to know you better in the next phase of our selection process.
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <div style="display: inline-block; background: #27ae60; color: white; padding: 12px 30px; border-radius: 25px; font-weight: 600; font-size: 16px;">
                    ✨ Good Luck! ✨
                </div>
            </div>
        </div>
        
        <div style="background: #2c3e50; color: #bdc3c7; padding: 25px; text-align: center; border-radius: 0 0 10px 10px;">
            <p style="margin: 0 0 10px 0; font-size: 18px; font-weight: 600; color: #ecf0f1;">Best regards,</p>
            <p style="margin: 0; font-size: 16px; color: #95a5a6;">Recruitment Team</p>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #34495e;">
                <p style="margin: 0; font-size: 14px; color: #7f8c8d;">
                    This is an automated message. Please do not reply to this email.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

def send_outlook_email(sender_email, app_password, recipient_data, subject=None, body=None, use_html=True):
    # Default template values
    if subject is None:
        subject = "🎉 Application Update - You're Shortlisted!"

    success_count = 0
    failed_emails = []

    # Handle both old format (list of emails) and new format (list of dicts with email/test_link)
    if recipient_data and isinstance(recipient_data[0], str):
        # Old format - just email addresses
        recipient_data = [{'email': email, 'test_link': None, 'name': 'Candidate'} for email in recipient_data]
    elif isinstance(recipient_data, str):
        # Single email string
        recipient_data = [{'email': recipient_data, 'test_link': None, 'name': 'Candidate'}]

    for recipient in recipient_data:
        try:
            recipient_email = recipient['email']
            test_link = recipient.get('test_link', '')
            candidate_name = recipient.get('name', 'Candidate')
            
            # Create the email message
            message = MIMEMultipart('alternative')
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject

            # Generate personalized email body
            if body is None:
                if use_html:
                    email_body = get_html_template(test_link, candidate_name)
                else:
                    test_link_text = f"\n\nPlease complete your assessment: {test_link}\n" if test_link else ""
                    email_body = f"""Dear {candidate_name},

We are pleased to inform you that you have been shortlisted for the next round of our selection process.
{test_link_text}
You will soon be contacted by our HR team within the next 2-3 days. They will provide you with detailed instructions for the upcoming round and guide you through the next steps.

Thank you for your interest in joining our organization. We look forward to proceeding with your application.

Best regards,
Recruitment Team"""
            else:
                email_body = body

            # Add body to email
            if use_html:
                message.attach(MIMEText(email_body, 'html'))
            else:
                message.attach(MIMEText(email_body, 'plain'))

            # Connect to Outlook SMTP server
            server = smtplib.SMTP(os.getenv('SMTP_SERVER'), os.getenv('SMTP_PORT'))
            server.starttls()  # Secure the connection
            server.login(sender_email, app_password)
            server.send_message(message)
            server.quit()
            
            print(f"Email sent successfully to {recipient_email}" + (f" with test link: {test_link}" if test_link else ""))
            success_count += 1
            
        except Exception as e:
            print(f"Failed to send email to {recipient.get('email', 'unknown')}: {e}")
            failed_emails.append(recipient.get('email', 'unknown'))
    
    print(f"\nSummary: {success_count} emails sent successfully")
    if failed_emails:
        print(f"Failed to send to: {', '.join(failed_emails)}")