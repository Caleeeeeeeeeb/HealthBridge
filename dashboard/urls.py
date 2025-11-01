from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Old unified dashboard (kept for compatibility)
    path('donor/', views.donor_dashboard, name='donor_dashboard'),
    path('recipient/', views.recipient_dashboard, name='recipient_dashboard'),
]
