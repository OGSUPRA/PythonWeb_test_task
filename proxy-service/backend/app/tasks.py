from app.celery_app import celery_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

@celery_app.task
def send_activation_email_task(email: str, activation_key: str):
    """Отправка письма с ключом активации"""
    try:
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_USER
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
        
        # Для теста используем вывод в консоль, если SMTP не настроен
        if settings.SMTP_HOST == "smtp.mailtrap.io" and settings.SMTP_USER == "your_mailtrap_user":
            print(f"\n{'='*50}")
            print(f"EMAIL WOULD BE SENT TO: {email}")
            print(f"ACTIVATION KEY: {activation_key}")
            print(f"{'='*50}\n")
            return
        
        # Реальная отправка
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            
    except Exception as e:
        print(f"Failed to send email: {e}")