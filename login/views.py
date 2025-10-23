from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.shortcuts import redirect, render

User = get_user_model()


def login_view(request):
    """User login view"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        return render(request, "login/login.html", {"error": "Invalid credentials"})
    return render(request, "login/login.html")


def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect("landing:home")


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
