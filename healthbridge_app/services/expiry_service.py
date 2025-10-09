"""
Expiry monitoring utilities and services for HealthBridge
"""
from datetime import date, timedelta
from django.core.mail import send_mass_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from typing import List, Dict, Any

from .models import Donation, ExpiryAlert


class ExpiryMonitoringService:
    """Service class for handling expiry monitoring operations"""
    
    def __init__(self):
        self.User = get_user_model()
    
    def get_expiring_donations(self, days_ahead: int = 10) -> Dict[str, Any]:
        """Get donations grouped by urgency level"""
        donations = Donation.objects.expiring_within(days=days_ahead)
        
        today = date.today()
        
        return {
            'critical': donations.filter(expiry_date__lte=today + timedelta(days=1)),
            'high': donations.filter(
                expiry_date__gt=today + timedelta(days=1),
                expiry_date__lte=today + timedelta(days=3)
            ),
            'medium': donations.filter(
                expiry_date__gt=today + timedelta(days=3),
                expiry_date__lte=today + timedelta(days=7)
            ),
            'low': donations.filter(
                expiry_date__gt=today + timedelta(days=7),
                expiry_date__lte=today + timedelta(days=days_ahead)
            ),
        }
    
    def get_notification_stats(self, days_back: int = 7) -> Dict[str, int]:
        """Get statistics about recent notifications"""
        since_date = timezone.now() - timedelta(days=days_back)
        
        alerts = ExpiryAlert.objects.filter(alert_sent_at__gte=since_date)
        
        return {
            'total_alerts': alerts.count(),
            'unique_donations': alerts.values('donation').distinct().count(),
            'unique_recipients': alerts.values('recipient_email').distinct().count(),
            'email_alerts': alerts.filter(alert_type='email').count(),
        }
    
    def get_user_expiry_summary(self, user) -> Dict[str, Any]:
        """Get expiry summary for a specific user"""
        if not user.is_authenticated:
            return {}
        
        user_donations = Donation.objects.filter(donor=user)
        expiring = user_donations.expiring_within(days=10)
        
        return {
            'total_donations': user_donations.count(),
            'expiring_donations': expiring.count(),
            'critical_expiring': expiring.filter(expiry_date__lte=date.today() + timedelta(days=3)).count(),
            'expired_donations': user_donations.expired().count(),
        }
    
    def should_send_reminder(self, donation: Donation, recipient_email: str) -> bool:
        """Check if a reminder should be sent based on business rules"""
        days_until_expiry = donation.days_until_expiry
        
        # Don't send for expired medicines
        if days_until_expiry < 0:
            return False
        
        # Check if already notified for this specific timeframe
        existing_alert = ExpiryAlert.objects.filter(
            donation=donation,
            days_before_expiry=days_until_expiry,
            recipient_email=recipient_email
        ).first()
        
        if existing_alert:
            # For critical medicines, allow re-notification after 24 hours
            if days_until_expiry <= 1 and not existing_alert.was_sent_recently:
                return True
            return False
        
        return True
    
    def get_urgency_emoji(self, urgency_level: str) -> str:
        """Get emoji for urgency level"""
        emoji_map = {
            'critical': '🚨',
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢',
            'normal': '⚪',
            'expired': '❌'
        }
        return emoji_map.get(urgency_level, '⚪')
    
    def format_expiry_message(self, donation: Donation) -> str:
        """Format a user-friendly expiry message"""
        days = donation.days_until_expiry
        urgency = donation.urgency_level
        emoji = self.get_urgency_emoji(urgency)
        
        if days < 0:
            return f"{emoji} Expired {abs(days)} day{'s' if abs(days) != 1 else ''} ago"
        elif days == 0:
            return f"{emoji} Expires TODAY"
        elif days == 1:
            return f"{emoji} Expires TOMORROW"
        else:
            return f"{emoji} Expires in {days} days"


# Convenience function for templates
def get_expiry_service():
    """Get an instance of the expiry monitoring service"""
    return ExpiryMonitoringService()