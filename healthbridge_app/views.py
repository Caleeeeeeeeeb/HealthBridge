from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    return render(request, 'healthbridge_app/home.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = email  # generate username

        if User.objects.filter(email=email).exists():
            return render(request, 'healthbridge_app/register.html', {'error': 'Email already exists'})

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return redirect('login')

    return render(request, 'healthbridge_app/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # username=email because USERNAME_FIELD=email
        user = authenticate(request, email=email, password=password)
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
    return redirect('home')
