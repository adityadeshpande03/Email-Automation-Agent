from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from agents.email_agent import process_email_with_test_link, process_email_input
import uvicorn

app = FastAPI(
    title="Email Automation API",
    description="API for sending automated shortlisting emails to candidates",
    version="1.0.0"
)

class EmailWithTestLinkRequest(BaseModel):
    email_input: str = Field(..., description="Email address of the candidate")
    test_link: str = Field(..., description="Test link to send to candidate")
    candidate_name: str = Field(default="Candidate", description="Name of the candidate")

class BulkEmailRequest(BaseModel):
    email_input: str = Field(..., description="Email addresses (comma or space separated)")

class EmailResponse(BaseModel):
    success: bool
    message: str

@app.post("/send-email-with-test-link", response_model=EmailResponse)
async def send_email_with_test_link(request: EmailWithTestLinkRequest):
    """Send email with test link to candidate"""
    try:
        result = process_email_with_test_link(
            email_input=request.email_input,
            test_link=request.test_link,
            candidate_name=request.candidate_name
        )
        
        if "Successfully sent" in result:
            return EmailResponse(success=True, message=result)
        else:
            return EmailResponse(success=False, message=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.post("/send-bulk-emails", response_model=EmailResponse)
# async def send_bulk_emails(request: BulkEmailRequest):
#     """Send emails to multiple candidates"""
#     try:
#         result = process_email_input(email_input=request.email_input)
        
#         if "Successfully sent" in result:
#             return EmailResponse(success=True, message=result)
#         else:
#             return EmailResponse(success=False, message=result)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Email Automation API",
        "endpoints": {
            "send_email_with_test_link": "/send-email-with-test-link",
            "send_bulk_emails": "/send-bulk-emails",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
