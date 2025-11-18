"""
Simple script to test email configuration
Run this to verify email settings work before deploying
"""
import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    # Display current email settings
    print(f"\n📧 Email Backend: {settings.EMAIL_BACKEND}")
    print(f"📧 Email Host: {settings.EMAIL_HOST}")
    print(f"📧 Email Port: {settings.EMAIL_PORT}")
    print(f"📧 Email User: {settings.EMAIL_HOST_USER}")
    print(f"📧 Email Password: {'*' * len(str(settings.EMAIL_HOST_PASSWORD)) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"📧 Default From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"📧 Use TLS: {settings.EMAIL_USE_TLS}")
    
    # Check if credentials are configured
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("\n❌ ERROR: Email credentials not configured!")
        print("Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your .env file")
        return False
    
    # Ask for test email address
    print("\n" + "=" * 60)
    test_email = input("Enter your email address to send a test email: ").strip()
    
    if not test_email:
        print("❌ No email address provided. Test cancelled.")
        return False
    
    print(f"\n🔄 Sending test email to {test_email}...")
    
    try:
        # Send test email
        result = send_mail(
            subject='HealthBridge - Email Configuration Test',
            message='This is a test email from HealthBridge. If you received this, your email configuration is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        if result == 1:
            print("\n✅ SUCCESS! Test email sent successfully!")
            print(f"✅ Check {test_email} for the test message")
            print("\n✨ Your email configuration is working correctly!")
            return True
        else:
            print("\n❌ FAILED: Email was not sent (result = 0)")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: Failed to send email")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Error message: {str(e)}")
        print("\n💡 Common issues:")
        print("   1. Gmail blocking login - Enable 'Less secure app access' or use App Password")
        print("   2. Wrong credentials - Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
        print("   3. Network issues - Check your internet connection")
        print("   4. Gmail 2FA - You need to create an App Password at myaccount.google.com/apppasswords")
        return False

if __name__ == "__main__":
    try:
        test_email()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    
    print("\n" + "=" * 60)
    input("Press Enter to exit...")
