"""Environment configuration; retain existing defaults."""
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "visa-culture-secret")
    SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.hostinger.com")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
    BOOKING_RECIPIENTS = os.environ.get(
        "BOOKING_RECIPIENTS",
        "shahidorganchemist@gmail.com,info@visaculture.com",
    )
    TURNSTILE_SITEKEY = os.environ.get("TURNSTILE_SITEKEY", "")
    TURNSTILE_SECRET_KEY = os.environ.get("TURNSTILE_SECRET_KEY", "")
