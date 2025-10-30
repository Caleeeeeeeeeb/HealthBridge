from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# NEW
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib import messages

User = get_user_model()

@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, "✅ Profile updated successfully.")
        return redirect('dashboard:dashboard')
    return render(request, 'profile/edit_profile.html', {'user': request.user})

#change pass
class ProfilePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'profile/change_password.html'
    success_url = reverse_lazy('profile:password_change_done')

    def form_valid(self, form):
        messages.success(self.request, "✅ Password updated successfully.")
        return super().form_valid(form)

class ProfilePasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'profile/change_password_done.html'