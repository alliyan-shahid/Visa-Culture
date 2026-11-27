"""Booking email integration."""
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import parseaddr
from flask import current_app


def _valid_reply_to(value):
    """Return a safe reply-to address or an empty string."""
    if not value or "\r" in value or "\n" in value:
        return ""
    _, address = parseaddr(value)
    return address if "@" in address else ""


def send_booking_email(form_data):
    sender = current_app.config["SMTP_USER"]
    password = current_app.config["SMTP_PASSWORD"]
    recipients = [
        address.strip()
        for address in current_app.config["BOOKING_RECIPIENTS"].split(",")
        if address.strip()
    ]
    if not sender or not password or not recipients:
        raise RuntimeError("Booking email settings are not configured")

    fields = [
        ("Full name", form_data.get("name") or "Not provided"),
        ("Phone number", form_data.get("phone") or "Not provided"),
        ("Email address", form_data.get("email") or "Not provided"),
        ("Service type", form_data.get("service_type") or "Not provided"),
        ("Preferred date", form_data.get("date") or "Not provided"),
        (
            "Preferred test" if form_data.get("service_type") == "test_preparation" else "Preferred destination",
            form_data.get("university") or "Not provided",
        ),
        ("Address", form_data.get("address") or "Not provided"),
        ("Message", form_data.get("message") or "Not provided"),
    ]
    details = "\n".join(f"{label}: {value}" for label, value in fields)

    applicant_email = _valid_reply_to(form_data.get("email", "").strip())

    message = EmailMessage()
    message["Subject"] = f"New Consultation Booking Request | {form_data.get('name') or 'Website Visitor'} | Visa Culture"
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    if applicant_email:
        message["Reply-To"] = applicant_email
    message.set_content(
        "A new consultation request was submitted through the Visa Culture booking form.\n\n"
        "BOOKING DETAILS\n"
        "================\n"
        f"{details}\n\n"
        "Please follow up with the applicant using the details above."
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(current_app.config["SMTP_HOST"], current_app.config["SMTP_PORT"], context=context) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
        if applicant_email:
            confirmation = EmailMessage()
            confirmation["Subject"] = "Booking Received — Visa Culture Will Contact You Soon"
            confirmation["From"] = sender
            confirmation["To"] = applicant_email
            confirmation.set_content(
                f"Dear {form_data.get('name') or 'Applicant'},\n\n"
                "Thank you for contacting Visa Culture. We have received your booking request successfully.\n\n"
                "Our team will review your details and contact you shortly regarding the next steps.\n\n"
                "Regards,\n"
                "Visa Culture Team\n"
                "info@visaculture.com"
            )
            smtp.send_message(confirmation)
