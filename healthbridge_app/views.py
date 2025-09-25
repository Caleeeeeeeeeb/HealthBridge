from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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
    return render(request, 'healthbridge_app/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
