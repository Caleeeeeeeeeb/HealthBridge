from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from donations.models import Donation, ExpiryAlert
from requests.models import MedicineRequest


@login_required
def dashboard(request):
    """Unified dashboard view combining donor and recipient features"""
    context = {}
    
    # ===== DONOR STATISTICS =====
    total_donations = Donation.objects.filter(donor=request.user).count()
    available_donations = Donation.objects.filter(donor=request.user, status='available').count()
    reserved_donations = Donation.objects.filter(donor=request.user, status='reserved').count()
    delivered_donations = Donation.objects.filter(donor=request.user, status='delivered').count()
    
    # Get recent donations (last 5)
    recent_donations = Donation.objects.filter(donor=request.user).order_by('-donated_at')[:5]
    
    # Expiring donations warning
    user_expiring = Donation.objects.expiring_within(days=10).filter(donor=request.user)
    critical_donations = user_expiring.filter(expiry_date__lte=date.today() + timedelta(days=3))
    
    context.update({
        'total_donations': total_donations,
        'available_donations': available_donations,
        'reserved_donations': reserved_donations,
        'delivered_donations': delivered_donations,
        'recent_donations': recent_donations,
        'user_expiring_donations': user_expiring,
        'user_critical_donations': critical_donations,
    })
    
    # ===== RECIPIENT STATISTICS =====
    user_requests = MedicineRequest.objects.filter(recipient=request.user)
    
    context.update({
        'total_requests': user_requests.count(),
        'pending_requests': user_requests.filter(status=MedicineRequest.Status.PENDING).count(),
        'matched_requests': user_requests.filter(status=MedicineRequest.Status.MATCHED).count(),
        'available_medicines': Donation.objects.filter(status=Donation.Status.AVAILABLE).count(),
        'recent_requests': user_requests.order_by('-created_at')[:5],
    })
    
    # Admin features (if staff)
    if request.user.is_staff:
        all_expiring = Donation.objects.expiring_within(days=14)
        
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
        context['recent_alerts'] = ExpiryAlert.objects.filter(
            alert_sent_at__gte=timezone.now() - timedelta(days=7)
        ).select_related('donation')[:10]
    
    return render(request, "dashboard/dashboard.html", context)


@login_required
def donor_dashboard(request):
    """Professional Donor Dashboard - View and manage medicine donations"""
    # Ensure user is a donor
    if not request.user.is_donor:
        return redirect('dashboard:recipient_dashboard' if request.user.is_recipient else 'select_role')
    
    context = {}
    
    # Donor statistics
    total_donations = Donation.objects.filter(donor=request.user).count()
    available_donations = Donation.objects.filter(donor=request.user, status=Donation.Status.AVAILABLE).count()
    reserved_donations = Donation.objects.filter(donor=request.user, status=Donation.Status.RESERVED).count()
    delivered_donations = Donation.objects.filter(donor=request.user, status=Donation.Status.DELIVERED).count()
    
    # Recent donations
    recent_donations = Donation.objects.filter(donor=request.user).order_by('-donated_at')[:10]
    
    # Expiring donations warning
    user_expiring = Donation.objects.expiring_within(days=10).filter(donor=request.user)
    critical_donations = user_expiring.filter(expiry_date__lte=date.today() + timedelta(days=3))
    
    # Requests for donor's medicines
    matched_requests = MedicineRequest.objects.filter(
        matched_donation__donor=request.user
    ).order_by('-created_at')[:5]
    
    context.update({
        'total_donations': total_donations,
        'available_donations': available_donations,
        'reserved_donations': reserved_donations,
        'delivered_donations': delivered_donations,
        'recent_donations': recent_donations,
        'user_expiring_donations': user_expiring,
        'user_critical_donations': critical_donations,
        'matched_requests': matched_requests,
    })
    
    return render(request, "dashboard/donor_dashboard.html", context)


@login_required
def recipient_dashboard(request):
    """Professional Recipient Dashboard - View and request medicines"""
    # Ensure user is a recipient
    if not request.user.is_recipient:
        return redirect('dashboard:donor_dashboard' if request.user.is_donor else 'select_role')
    
    context = {}
    
    # Recipient statistics
    user_requests = MedicineRequest.objects.filter(recipient=request.user)
    
    total_requests = user_requests.count()
    pending_requests = user_requests.filter(status=MedicineRequest.Status.PENDING).count()
    matched_requests = user_requests.filter(status=MedicineRequest.Status.MATCHED).count()
    fulfilled_requests = user_requests.filter(status=MedicineRequest.Status.FULFILLED).count()
    
    # Available medicines
    available_medicines = Donation.objects.filter(status=Donation.Status.AVAILABLE).order_by('expiry_date')[:10]
    available_medicines_count = Donation.objects.filter(status=Donation.Status.AVAILABLE).count()
    
    # Recent requests
    recent_requests = user_requests.order_by('-created_at')[:10]
    
    # Claimed medicines
    try:
        from requests.models import ClaimedMedicine
        claimed_medicines = ClaimedMedicine.objects.filter(recipient=request.user).order_by('-claimed_at')[:5]
        total_claimed = ClaimedMedicine.objects.filter(recipient=request.user).count()
    except:
        claimed_medicines = []
        total_claimed = 0
    
    context.update({
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'matched_requests': matched_requests,
        'fulfilled_requests': fulfilled_requests,
        'available_medicines': available_medicines,
        'available_medicines_count': available_medicines_count,
        'recent_requests': recent_requests,
        'claimed_medicines': claimed_medicines,
        'total_claimed': total_claimed,
    })
    
    return render(request, "dashboard/recipient_dashboard.html", context)
