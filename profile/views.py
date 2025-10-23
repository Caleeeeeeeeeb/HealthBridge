from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def profile_view(request):
    """Display user profile"""
    user = request.user
    
    # Count user's donations and requests
    donations_count = user.donation_set.count() if hasattr(user, 'donation_set') else 0
    requests_count = user.medicinerequest_set.count() if hasattr(user, 'medicinerequest_set') else 0
    
    context = {
        'user': user,
        'donations_count': donations_count,
        'requests_count': requests_count,
    }
    
    return render(request, 'profile/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('profile:profile')
    
    return render(request, 'profile/edit_profile.html', {'user': request.user})

