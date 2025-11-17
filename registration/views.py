from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

User = get_user_model()


def register(request):
    """User registration view"""
    # Redirect authenticated users to their dashboard
    if request.user.is_authenticated:
        if not request.user.role_selected:
            return redirect("select_role")
        if request.user.is_donor:
            return redirect("dashboard:donor_dashboard")
        elif request.user.is_recipient:
            return redirect("dashboard:recipient_dashboard")
        return redirect("landing:home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        username = email

        if User.objects.filter(email=email).exists():
            return render(request, "registration/register.html", {"error": "Email already exists"})

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
        )
        return redirect("login:login")

    return render(request, "registration/register.html")
