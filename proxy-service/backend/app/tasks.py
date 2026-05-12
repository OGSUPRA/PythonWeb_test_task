import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.celery_app import celery_app
from app.config import settings


@celery_app.task
def send_activation_email_task(email: str, activation_key: str):
    """Send the one-time activation key to the user's email."""
    try:
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = email
        msg["Subject"] = "Your Proxy Service Activation Key"

        body = f"""
        Hello!

        Your activation key: {activation_key}

        Use this key in the desktop application to connect to the proxy server.

        The key is valid for 7 days or until first use.

        Best regards,
        Proxy Service
        """

        msg.attach(MIMEText(body, "plain"))

        if settings.EMAIL_BACKEND == "console" or settings.SMTP_USER in {
            "",
            "mailtrap_username",
            "your_mailtrap_user",
        }:
            print(f"\n{'='*50}")
            print(f"EMAIL WOULD BE SENT TO: {email}")
            print(f"ACTIVATION KEY: {activation_key}")
            print("Set EMAIL_BACKEND=smtp and real SMTP credentials to send actual emails.")
            print(f"{'='*50}\n")
            return

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

    except Exception as exc:
        print(f"Failed to send email: {exc}")
