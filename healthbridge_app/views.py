from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.text import slugify
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from .models import Donation

User = get_user_model()


def home(request):
    return render(request, 'healthbridge_app/home.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = email  # use email as username

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


# ✅ SEARCH VIEW FIXED (no more medicine_name)
def medicine_search(request):
    query = request.GET.get('q', '')
    medicines = Donation.objects.all()

    # filter using "name" (your actual model field)
    if query:
        medicines = medicines.filter(name__icontains=query)

    # optional filename mapping (so image lookup works)
    NAME_MAP = {
        'biogisic': 'biogesic',
        'tambal ubo': 'tambalubo',
        'para': 'para',
        'gay': 'gay',
        'test1': 'test1',
        'test2': 'test2',
        'paracetamol': 'Paracetamol',
    }

    for med in medicines:
        med_name = med.name.lower().strip()  # ✅ fixed
        base = NAME_MAP.get(med_name, slugify(med.name))
        candidates = [f'medicines/{base}.png', f'medicines/{base}.jpg']

        chosen = None
        for rel in candidates:
            if finders.find(rel):
                chosen = static(rel)
                break

        # this attaches an accessible image URL to each medicine
        med.image_static = chosen or static('img/placeholder-medicine.png')

    return render(request, 'healthbridge_app/medicine_search.html', {
        'medicines': medicines,
        'query': query
    })


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
