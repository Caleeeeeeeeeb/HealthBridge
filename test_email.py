import os
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("EMAIL CONFIGURATION TEST")
print("=" * 60)
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print("=" * 60)

# Test sending email
try:
    print("\nAttempting to send test email...")
    send_mail(
        subject='HealthBridge Test Email',
        message='This is a test email from HealthBridge. If you receive this, email is working correctly!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],  # Send to yourself
        fail_silently=False,
    )
    print("✅ SUCCESS! Test email sent successfully!")
    print(f"Check inbox: {settings.EMAIL_HOST_USER}")
except Exception as e:
    print(f"❌ ERROR: Failed to send email")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nPossible issues:")
    print("1. App Password is incorrect or has spaces")
    print("2. 2-Step Verification not enabled on Gmail")
    print("3. Network/firewall blocking SMTP connection")
    print("4. Gmail account settings blocking 'less secure apps'")

print("\n" + "=" * 60)
