from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return None
        
        try:
            # Normalize email and handle whitespace
            email = email.strip().lower()
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Run the default password hasher to reduce timing attacks
            User().set_password(password)
            logger.warning(f"Authentication failed: User not found for email {email}")
            return None
        except Exception as e:
            logger.error(f"Error during authentication: {str(e)}")
            return None
        
        try:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception as e:
            logger.error(f"Error checking password for user {email}: {str(e)}")
            return None
        
        return None