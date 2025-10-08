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

# this is for medicine search list
from django.shortcuts import render
from .services.medicine_service import MedicineService

from .models import Donation
def medicine_search(request):
    query = request.GET.get('q', '')
    medicines = Donation.objects.all()

    if query:
        medicines = medicines.filter(medicine_name__icontains=query)

    return render(request, 'healthbridge_app/medicine_search.html', {
        'medicines': medicines,
        'query': query
    })


from .models import GenericMedicine, BrandMedicine
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import GenericMedicine


from .models import Donation
def donate_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        expiry_date = request.POST.get('expiry_date')
        

        if name and quantity and expiry_date:
            Donation.objects.create(
                name=name,
                quantity=quantity,
                expiry_date=expiry_date
            )
            messages.success(request, f"Thank you for donating {quantity}x {name}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'healthbridge_app/donate_medicine.html')