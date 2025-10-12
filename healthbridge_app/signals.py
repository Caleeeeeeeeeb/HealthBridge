"""
Real-time expiry monitoring using Django signals
This triggers immediately when donations are added/updated
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Donation, ExpiryAlert

@receiver(post_save, sender=Donation)
def check_expiry_on_donation_save(sender, instance, created, **kwargs):
    """
    Automatically check expiry when a donation is created or updated
    """
    if instance.expiry_date:
        # Ensure expiry_date is a date object
        from datetime import datetime, date
        
        expiry_date = instance.expiry_date
        if isinstance(expiry_date, str):
            try:
                expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            except ValueError:
                print(f"❌ Invalid date format: {expiry_date}")
                return
        
        days_until_expiry = (expiry_date - timezone.now().date()).days
        
        # Check if this donation needs immediate attention
        if days_until_expiry <= 10:  # Within 10 days
            print(f"🚨 REAL-TIME ALERT: {instance.name} expires in {days_until_expiry} days!")
            
            # Determine urgency level
            urgency = "CRITICAL" if days_until_expiry <= 3 else "WARNING" if days_until_expiry <= 7 else "LOW"
            print(f"📊 Urgency Level: {urgency} | Expiry Date: {expiry_date}")
            
            # AUTOMATICALLY SEND EMAILS in real-time
            try:
                from .management.commands.check_expiry import Command as ExpiryCommand
                expiry_command = ExpiryCommand()
                
                # Provide default options for the command
                default_options = {
                    'days': 10,
                    'dry_run': False,  # Send real emails
                    'force': True,     # Override duplicate protection for real-time
                    'critical_only': days_until_expiry <= 3,  # Only critical if very urgent
                    'verbosity': 1
                }
                
                print(f"📧 Automatically sending email alerts to staff...")
                expiry_command.handle(**default_options)
                print(f"✅ Real-time email alerts sent successfully!")
                
            except Exception as e:
                print(f"⚠️ Real-time email failed: {e}")
                print(f"💡 Fallback: Daily automation will catch this at 9:00 AM")

@receiver(post_delete, sender=Donation)
def cleanup_alerts_on_donation_delete(sender, instance, **kwargs):
    """
    Clean up alerts when donation is deleted
    """
    ExpiryAlert.objects.filter(donation=instance).delete()
    print(f"🗑️ Cleaned up alerts for deleted donation: {instance.name}")