from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from donations.models import Donation, ExpiryAlert
from requests.models import MedicineRequest


@login_required
def dashboard(request):
    """Donor dashboard view"""
    context = {}
    
    # If user is authenticated, show their expiring donations
    if request.user.is_authenticated:
        # Get user's donations expiring within 10 days using custom manager
        user_expiring = Donation.objects.expiring_within(days=10).filter(donor=request.user)
        context['user_expiring_donations'] = user_expiring
        context['user_critical_donations'] = user_expiring.filter(expiry_date__lte=date.today() + timedelta(days=3))
        
        # If user is admin/staff, show all expiring donations with urgency levels
        if request.user.is_staff:
            all_expiring = Donation.objects.expiring_within(days=14)
            
            # Group by urgency for better dashboard display
            context['critical_donations'] = all_expiring.filter(expiry_date__lte=date.today() + timedelta(days=1))
            context['high_priority_donations'] = all_expiring.filter(
                expiry_date__gt=date.today() + timedelta(days=1),
                expiry_date__lte=date.today() + timedelta(days=3)
            )
            context['medium_priority_donations'] = all_expiring.filter(
                expiry_date__gt=date.today() + timedelta(days=3),
                expiry_date__lte=date.today() + timedelta(days=7)
            )
            context['low_priority_donations'] = all_expiring.filter(
                expiry_date__gt=date.today() + timedelta(days=7)
            )
            
            context['total_expiring_count'] = all_expiring.count()
            
            # Recent alerts for admin
            context['recent_alerts'] = ExpiryAlert.objects.filter(
                alert_sent_at__gte=timezone.now() - timedelta(days=7)
            ).select_related('donation')[:10]
    
    return render(request, "dashboard/dashboard.html", context)


@login_required
def recipient_dashboard(request):
    """Recipient dashboard view"""
    user_requests = MedicineRequest.objects.filter(recipient=request.user)
    
    context = {
        'total_requests': user_requests.count(),
        'pending_requests': user_requests.filter(status=MedicineRequest.Status.PENDING).count(),
        'matched_requests': user_requests.filter(status=MedicineRequest.Status.MATCHED).count(),
        'available_medicines': Donation.objects.filter(status=Donation.Status.AVAILABLE).count(),
        'recent_requests': user_requests.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/recipient.html', context)
