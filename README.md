# Email Automation Agent

A FastAPI-based service for sending automated shortlisting emails to candidates, with optional test links. Supports both single and bulk email sending.

## Features

- Send personalized shortlisting emails to candidates.
- Optionally include a test/assessment link in the email.
- Bulk email support (commented in code, can be enabled).
- HTML email templates for professional appearance.
- Uses Outlook SMTP (Office365) for sending emails.
- API endpoints for integration.

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies.

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   Create a `.env` file in the project root (see `.env` example below):

   ```
   # GOOGLE GEMINI CONFIGURATION
   GEMINI_API_KEY=your_gemini_api_key

   # SMTP CONFIGURATION
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=your_email@gmail.com
   APP_PASSWORD=your_app_password
   ```

   - For Outlook, generate an app password if using MFA.

4. **Run the API:**
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `POST /send-email-with-test-link`  
  Send a shortlisting email with a test link to a candidate.

  **Request Body:**
  ```json
  {
    "email_input": "candidate@example.com",
    "test_link": "https://your-test-link.com",
    "candidate_name": "John Doe"
  }
  ```

- `GET /`  
  API info and available endpoints.

- `GET /health`  
  Health check endpoint.

## Customization

- Email templates can be modified in `tools/smtp_connection.py`.
- Bulk email endpoint is available in code but commented out in `main.py`.

## Notes

- Ensure your SMTP credentials are correct and have permission to send emails.
- This is an automated system; do not reply to the sent emails.


