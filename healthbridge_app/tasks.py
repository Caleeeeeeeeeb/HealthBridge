"""
Background task monitoring using Celery
Runs continuous monitoring in the background
"""
from celery import Celery
from django.utils import timezone
from datetime import timedelta
import time

# Create Celery app
app = Celery('healthbridge_expiry')

@app.task
def continuous_expiry_monitor():
    """
    Continuously monitor for expiring medicines
    More efficient than daily checks
    """
    from healthbridge_app.models import Donation
    from healthbridge_app.management.commands.check_expiry import Command as ExpiryCommand
    
    while True:
        # Check every 4 hours instead of daily
        current_time = timezone.now()
        
        # Quick check - only run full check if we might have new expiring items
        near_expiry = Donation.objects.filter(
            expiry_date__lte=current_time.date() + timedelta(days=10),
            expiry_date__gte=current_time.date()
        ).count()
        
        if near_expiry > 0:
            print(f"🔍 Found {near_expiry} items approaching expiry - running full check")
            expiry_command = ExpiryCommand()
            expiry_command.handle(verbosity=1)
        else:
            print("✅ No items approaching expiry")
        
        # Wait 4 hours before next check
        time.sleep(14400)  # 4 hours = 14400 seconds

@app.task
def immediate_expiry_check(donation_id):
    """
    Immediate check for a specific donation
    Triggered when donations are added/updated
    """
    from healthbridge_app.models import Donation
    from healthbridge_app.management.commands.check_expiry import Command as ExpiryCommand
    
    try:
        donation = Donation.objects.get(id=donation_id)
        if donation.expiry_date:
            days_until_expiry = (donation.expiry_date - timezone.now().date()).days
            
            if days_until_expiry <= 10:
                print(f"⚡ IMMEDIATE CHECK: {donation.medicine_name} expires in {days_until_expiry} days")
                expiry_command = ExpiryCommand()
                expiry_command.handle(force=True)
    except Donation.DoesNotExist:
        pass