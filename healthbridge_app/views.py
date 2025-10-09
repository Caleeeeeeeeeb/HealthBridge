from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
    return render(request, "healthbridge_app/dashboard.html")

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
