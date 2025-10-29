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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Modular apps
    path('', include('landing.urls')),  # Landing page at root
    path('login/', include('login.urls')),  # Login, logout, and password reset
    path('register/', include('registration.urls')),  # Registration
    path('dashboard/', include('dashboard.urls')),  # Dashboards
    path('profile/', include('profile.urls')),  # User profile
    path('donations/', include('donations.urls')),  # Donations
    path('requests/', include('requests.urls')),  # Medicine requests
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
