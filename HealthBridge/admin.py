"""
Custom Django Admin Configuration
Adds a link back to the Admin Dashboard in the Django admin interface
"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class CustomAdminSite(admin.AdminSite):
    site_header = "HealthBridge Administration"
    site_title = "HealthBridge Admin"
    index_title = "Database Management"
    
    def each_context(self, request):
        """Add custom context to all admin pages"""
        context = super().each_context(request)
        # Add link to admin dashboard
        context['admin_dashboard_url'] = reverse('admin_dashboard')
        return context


# Create custom admin site instance
admin_site = CustomAdminSite(name='custom_admin')
