from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

User = get_user_model()


def register(request):
    """User registration view"""
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
        return redirect("login:login")

    return render(request, "registration/register.html")
