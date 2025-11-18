from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def login_view(request):
    """User login view"""
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
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Check if user has selected their role
            if not user.role_selected:
                return redirect("select_role")
            # Redirect to appropriate dashboard based on role
            if user.is_donor:
                return redirect("dashboard:donor_dashboard")
            elif user.is_recipient:
                return redirect("dashboard:recipient_dashboard")
            return redirect("landing:home")
        return render(request, "login/login.html", {"error": "Invalid credentials"})
    return render(request, "login/login.html")


def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect("landing:home")


class CustomPasswordResetView(PasswordResetView):
    template_name = 'login/password_reset.html'
    email_template_name = 'login/password_reset_email.html'
    success_url = reverse_lazy('login:password_reset_done')
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to their dashboard
        if request.user.is_authenticated:
            if not request.user.role_selected:
                return redirect("select_role")
            if request.user.is_donor:
                return redirect("dashboard:donor_dashboard")
            elif request.user.is_recipient:
                return redirect("dashboard:recipient_dashboard")
            return redirect("landing:home")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Override to add error handling and logging"""
        try:
            # Log email configuration (without password)
            logger.info(f"Attempting to send password reset email via {settings.EMAIL_HOST}")
            logger.info(f"Email user: {settings.EMAIL_HOST_USER}")
            
            # Check if email is configured
            if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                logger.error("Email credentials not configured")
                messages.error(
                    self.request, 
                    "Email service is not configured properly. Please contact support."
                )
                return redirect('login:password_reset')
            
            # Try to send the email
            response = super().form_valid(form)
            logger.info("Password reset email sent successfully")
            return response
            
        except Exception as e:
            # Log the full error
            logger.error(f"Password reset email failed: {str(e)}", exc_info=True)
            messages.error(
                self.request,
                f"Unable to send password reset email. Error: {str(e)[:100]}. Please try again or contact support."
            )
            return redirect('login:password_reset')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'login/password_reset_done.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to their dashboard
        if request.user.is_authenticated:
            if not request.user.role_selected:
                return redirect("select_role")
            if request.user.is_donor:
                return redirect("dashboard:donor_dashboard")
            elif request.user.is_recipient:
                return redirect("dashboard:recipient_dashboard")
            return redirect("landing:home")
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'login/password_reset_confirm.html'
    success_url = reverse_lazy('login:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'login/password_reset_complete.html'
