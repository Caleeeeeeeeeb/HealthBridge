from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.conf import settings

from .models import Donation, GenericMedicine, BrandMedicine

User = get_user_model()

# ---------- BASIC PAGES ----------
def home(request):
    return render(request, "healthbridge_app/home.html")

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = email

        if User.objects.filter(email=email).exists():
            return render(request, "healthbridge_app/register.html", {"error": "Email already exists"})

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return redirect("login")

    return render(request, "healthbridge_app/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        return render(request, "healthbridge_app/login.html", {"error": "Invalid credentials"})
    return render(request, "healthbridge_app/login.html")

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
            from .models import ExpiryAlert
            context['recent_alerts'] = ExpiryAlert.objects.filter(
                alert_sent_at__gte=timezone.now() - timedelta(days=7)
            ).select_related('donation')[:10]
    
    return render(request, "healthbridge_app/dashboard.html", context)

def logout_view(request):
    logout(request)
    return redirect("home")

# ---------- SEARCH ----------
def medicine_search(request):
    query = request.GET.get('q', '').strip()
    medicines = Donation.objects.all()

    if query:
        medicines = medicines.filter(name__icontains=query)

    return render(request, 'healthbridge_app/medicine_search.html', {
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
            return redirect("dashboard")
        messages.error(request, "Please fill in all fields.")
    return render(request, "healthbridge_app/donate_medicine.html")

# ---------- TRACKING ----------
@login_required
def my_donations(request):
    items = Donation.objects.filter(donor=request.user).order_by("-donated_at")
    return render(request, "healthbridge_app/track_requests_list.html", {"items": items})

@login_required
def donation_detail(request, pk: int):
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)
    return render(request, "healthbridge_app/track_request_detail.html", {"donation": donation})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return redirect('forgot_password')

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')

        subject = 'Password Reset - HealthBridge'
        message = render_to_string('healthbridge_app/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        messages.success(request, 'Password reset link has been sent to your email.')
        return redirect('login')

    return render(request, 'healthbridge_app/forgot_password.html')

def reset_password(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'healthbridge_app/reset_password.html')
    else:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('forgot_password')