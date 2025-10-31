from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .models import GenericMedicine, BrandMedicine
from donations.models import Donation
from requests.models import MedicineRequest

User = get_user_model()

# ---------- BASIC PAGES ----------
def home(request):
    return render(request, "landing/home.html")

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = email

        if User.objects.filter(email=email).exists():
            return render(request, "registration/register.html", {"error": "Email already exists"})

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return redirect("login")

    return render(request, "registration/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        return render(request, "login/login.html", {"error": "Invalid credentials"})
    return render(request, "login/login.html")

def dashboard(request):
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
            from donations.models import ExpiryAlert
            context['recent_alerts'] = ExpiryAlert.objects.filter(
                alert_sent_at__gte=timezone.now() - timedelta(days=7)
            ).select_related('donation')[:10]
    
    return render(request, "dashboard/dashboard.html", context)

def logout_view(request):
    logout(request)
    return redirect("home")

# ---------- API ENDPOINTS ----------
def medicine_autocomplete(request):
    """API endpoint for medicine name autocomplete suggestions with caching"""
    query = request.GET.get('q', '').strip().lower()
    
    # Return empty if query too short
    if not query or len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Try to get from cache first (cache for 5 minutes)
    cache_key = f'autocomplete_{query}'
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return JsonResponse({'suggestions': cached_result})
    
    # Get unique medicine names from donations
    donation_medicines = Donation.objects.filter(
        name__icontains=query
    ).values_list('name', flat=True).distinct()[:5]
    
    # Get unique medicine names from generic medicines  
    generic_medicines = GenericMedicine.objects.filter(
        name__icontains=query
    ).values_list('name', flat=True).distinct()[:5]
    
    # Combine and deduplicate
    all_medicines = list(set(list(donation_medicines) + list(generic_medicines)))
    suggestions = sorted(all_medicines)[:10]  # Limit to 10 suggestions
    
    # Cache the result for 5 minutes (300 seconds)
    cache.set(cache_key, suggestions, 300)
    
    return JsonResponse({'suggestions': suggestions})

# ---------- SEARCH ----------
def medicine_search(request):
    query = request.GET.get('q', '').strip()
    medicines = Donation.objects.all()

    if query:
        medicines = medicines.filter(name__icontains=query)

    return render(request, 'donations/medicine_search.html', {
        'medicines': medicines,
        'query': query
    })

# ---------- DONATE ----------
@login_required
def donate_medicine(request):
    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        expiry_date = request.POST.get("expiry_date")
        image = request.FILES.get("image")

        if name and quantity and expiry_date:
            Donation.objects.create(
                name=name,
                quantity=quantity,
                expiry_date=expiry_date,
                donor=request.user,
                image=image,
            )
            messages.success(request, f"Thank you for donating {quantity}x {name}! You can track it under Track Requests.")
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Donation submitted successfully'})
            
            return redirect("dashboard")
        
        messages.error(request, "Please fill in all fields.")
        
        # Handle AJAX errors
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Please fill in all fields'}, status=400)
    
    return render(request, "donations/donate_medicine.html")

# ---------- TRACKING ----------
@login_required
def my_donations(request):
    items = Donation.objects.filter(donor=request.user).order_by("-donated_at")
    return render(request, "donations/track_requests_list.html", {"items": items})

@login_required
def donation_detail(request, pk: int):
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    return render(request, "donations/track_request_detail.html", {"donation": donation})


# ---------- DUPLICATE FUNCTIONS - NOW HANDLED BY dashboard AND requests APPS ----------
# recipient_dashboard, request_medicine, track_medicine_requests, medicine_request_detail
# are now handled in their respective apps (dashboard/views.py and requests/views.py)


@login_required
def delete_donation(request, pk):
    """Delete a donation (only by the donor)"""
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    
    if request.method == 'POST':
        medicine_name = donation.name
        donation.delete()
        messages.success(request, f'Donation "{medicine_name}" has been deleted successfully.')
        return redirect('dashboard')
    
    return render(request, 'donations/confirm_delete_donation.html', {'donation': donation})


@login_required
def delete_medicine_request(request, pk):
    """Delete a medicine request (only by the requester)"""
    medicine_request = get_object_or_404(MedicineRequest, pk=pk, recipient=request.user)
    
    if request.method == 'POST':
        medicine_name = medicine_request.medicine_name
        medicine_request.delete()
        messages.success(request, f'Request for "{medicine_name}" has been deleted successfully.')
        return redirect('track_medicine_requests')
    
    return render(request, 'requests/confirm_delete_request.html', {'medicine_request': medicine_request})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'login/password_reset.html'
    email_template_name = 'login/password_reset_email.html'
    success_url = '/password-reset-done/'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'login/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'login/password_reset_confirm.html'
    success_url = '/password-reset-complete/'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'login/password_reset_complete.html'