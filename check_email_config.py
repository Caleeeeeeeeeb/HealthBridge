"""
Diagnostic script to check email configuration on Render
This will help us see what's configured without exposing passwords in logs
"""
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 60)
print("EMAIL CONFIGURATION CHECK")
print("=" * 60)

# Check each environment variable
checks = {
    'EMAIL_HOST': os.getenv('EMAIL_HOST'),
    'EMAIL_PORT': os.getenv('EMAIL_PORT'),
    'EMAIL_HOST_USER': os.getenv('EMAIL_HOST_USER'),
    'EMAIL_HOST_PASSWORD': os.getenv('EMAIL_HOST_PASSWORD'),
}

for key, value in checks.items():
    if value:
        if 'PASSWORD' in key:
            print(f"✅ {key}: SET (length: {len(value)})")
        else:
            print(f"✅ {key}: {value}")
    else:
        print(f"❌ {key}: NOT SET")

print("=" * 60)
