from django.contrib import admin
from .models import Donation, ExpiryAlert


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'expiry_date', 'status', 'donor', 'tracking_code', 'donated_at']
    list_filter = ['status', 'expiry_date', 'donated_at']
    search_fields = ['name', 'tracking_code', 'donor__email']
    readonly_fields = ['tracking_code', 'donated_at', 'last_update']
    
    fieldsets = (
        ('Medicine Information', {
            'fields': ('name', 'quantity', 'expiry_date', 'image')
        }),
        ('Donor Information', {
            'fields': ('donor',)
        }),
        ('Status & Tracking', {
            'fields': ('status', 'tracking_code', 'notes')
        }),
        ('Timestamps', {
            'fields': ('donated_at', 'last_update'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExpiryAlert)
class ExpiryAlertAdmin(admin.ModelAdmin):
    list_display = ['donation', 'recipient_email', 'days_before_expiry', 'alert_type', 'alert_sent_at']
    list_filter = ['alert_type', 'alert_sent_at']
    search_fields = ['donation__name', 'recipient_email']
    readonly_fields = ['alert_sent_at']
