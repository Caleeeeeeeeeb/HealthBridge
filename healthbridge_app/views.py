from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .models import Medicine

def medicines_list(request):
    return render(request, 'healthbridge_app/medicines_list.html')

def home(request):
    return render(request, 'healthbridge_app/home.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            return render(request, 'healthbridge_app/register.html', {'error': 'Email already exists'})

        # Create user using email as username
        User.objects.create_user(username=email, email=email, password=password)
        return redirect('login')

    return render(request, 'healthbridge_app/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate using email as username
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'healthbridge_app/login.html', {'error': 'Invalid credentials'})

    return render(request, 'healthbridge_app/login.html')

def dashboard(request):
    medicines = Medicine.objects.all()[:24]  # sample list; tweak filters as needed
    return render(request, 'healthbridge_app/dashboard.html', {'medicines': medicines})
def logout_view(request):
    logout(request)
    return redirect('login')
def request_medicine(request, med_id):
    medicine = get_object_or_404(Medicine, id=med_id)
    # For now, just redirect back to dashboard (you can add logic later)
    return redirect('dashboard')