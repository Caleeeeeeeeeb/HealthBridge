# profile/urls.py
from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('edit/', views.edit_profile, name='edit_profile'),

    # NEW: change password + success
    path('password/change/', views.ProfilePasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', views.ProfilePasswordChangeDoneView.as_view(), name='password_change_done'),
]
