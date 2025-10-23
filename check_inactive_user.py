import os
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthBridge.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 60)
print("USER ACTIVATION STATUS CHECK")
print("=" * 60)

# Get the specific user
try:
    user = User.objects.get(email='rudyarddecember@gmail.com')
    
    print(f"\nUser: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is Active: {user.is_active}")
    print(f"Is Staff: {user.is_staff}")
    print(f"Is Superuser: {user.is_superuser}")
    print(f"Date Joined: {user.date_joined}")
    print(f"Last Login: {user.last_login}")
    
    print("\n" + "=" * 60)
    print("WHY A USER MIGHT BE INACTIVE:")
    print("=" * 60)
    print("1. Account was created but never activated (email verification)")
    print("2. Administrator manually deactivated the account")
    print("3. User was banned or suspended")
    print("4. Account deletion was requested (soft delete)")
    print("5. Failed login attempts triggered auto-deactivation")
    
    print("\n" + "=" * 60)
    print("TO ACTIVATE THIS USER:")
    print("=" * 60)
    print("Run this in Django shell or create an admin action:")
    print(f"   user = User.objects.get(email='rudyarddecember@gmail.com')")
    print(f"   user.is_active = True")
    print(f"   user.save()")
    
    # Ask if they want to activate
    print("\n" + "=" * 60)
    activate = input("Do you want to ACTIVATE this user now? (yes/no): ").strip().lower()
    
    if activate == 'yes':
        user.is_active = True
        user.save()
        print(f"\n✅ User {user.email} has been ACTIVATED!")
        print(f"   They can now log in and receive emails.")
    else:
        print("\nUser remains inactive.")
    
except User.DoesNotExist:
    print("User not found!")

print("\n" + "=" * 60)
