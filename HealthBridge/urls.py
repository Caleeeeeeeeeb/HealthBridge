"""
URL configuration for HealthBridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from healthbridge_app import views as hb_views
from healthbridge_app import admin_views
from healthbridge_app import notification_views

urlpatterns = [
    # Admin Dashboard & Approvals (must come before Django admin!)
    path('admin-dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/approve-donation/<int:donation_id>/', admin_views.approve_donation, name='approve_donation'),
    path('admin-dashboard/reject-donation/<int:donation_id>/', admin_views.reject_donation, name='reject_donation'),
    path('admin-dashboard/approve-request/<int:request_id>/', admin_views.approve_request, name='approve_request'),
    path('admin-dashboard/reject-request/<int:request_id>/', admin_views.reject_request, name='reject_request'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Role selection (one-time for new users)
    path('select-role/', hb_views.select_role, name='select_role'),
    
    # Notification API endpoints
    path('api/notifications/', notification_views.get_notifications, name='get_notifications'),
    path('api/notifications/unread-count/', notification_views.get_unread_count, name='get_unread_count'),
    path('api/notifications/<int:notification_id>/read/', notification_views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', notification_views.mark_all_read, name='mark_all_read'),
    
    # Notification page
    path('notifications/', notification_views.notifications_page, name='notifications_page'),
    
    # Modular apps
    path('', include('landing.urls')),  # Landing page at root
    path('login/', include('login.urls')),  # Login, logout, and password reset
    path('register/', include('registration.urls')),  # Registration
    path('dashboard/', include('dashboard.urls')),  # Dashboards
    path('profile/', include('profile.urls')),  # User profile
    path('donations/', include('donations.urls')),  # Donations
    path('requests/', include('requests.urls')),  # Medicine requests
]

# Custom error handlers
handler404 = 'HealthBridge.views.custom_404'
handler500 = 'HealthBridge.views.custom_500'

# Note: Media files are served from Supabase Storage (cloud), not locally
# No need for local media serving with Supabase Storage backend
