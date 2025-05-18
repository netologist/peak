import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.settings import get_settings

settings = get_settings()

def send_email_job(to_email: str, subject: str, body: str):
    message = MIMEMultipart()
    message["From"] = "noreply@example.com"
    message["To"] = to_email
    message["Subject"] = subject
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    # For demo purposes only - in production, use proper email config
    print(f"Email would be sent to {to_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")