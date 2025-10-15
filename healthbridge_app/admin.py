from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import CustomUser, GenericMedicine, BrandMedicine, Donation, ExpiryAlert, MedicineRequest


@admin.register(ExpiryAlert)
class ExpiryAlertAdmin(admin.ModelAdmin):
    list_display = ['donation_link', 'days_before_expiry', 'recipient_email', 'alert_type', 'alert_sent_at']
    list_filter = ['alert_type', 'days_before_expiry', 'alert_sent_at']
    search_fields = ['donation__name', 'recipient_email']
    readonly_fields = ['alert_sent_at']
    ordering = ['-alert_sent_at']
    date_hierarchy = 'alert_sent_at'
    
    def donation_link(self, obj):
        url = reverse('admin:healthbridge_app_donation_change', args=[obj.donation.pk])
        return format_html('<a href="{}">{}</a>', url, obj.donation.name)
    donation_link.short_description = 'Donation'
    donation_link.admin_order_field = 'donation__name'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'expiry_date', 'urgency_badge', 'status', 'donor', 'tracking_code']
    list_filter = ['status', 'expiry_date', 'donated_at']
    search_fields = ['name', 'tracking_code', 'donor__email']
    ordering = ['expiry_date']
    date_hierarchy = 'expiry_date'
    readonly_fields = ['tracking_code', 'donated_at', 'last_update', 'urgency_level', 'days_until_expiry']
    
    fieldsets = (
        ('Medicine Information', {
            'fields': ('name', 'quantity', 'expiry_date', 'image')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'tracking_code', 'notes')
        }),
        ('Donor Information', {
            'fields': ('donor',)
        }),
        ('Timestamps', {
            'fields': ('donated_at', 'last_update'),
            'classes': ('collapse',)
        }),
        ('Expiry Information', {
            'fields': ('urgency_level', 'days_until_expiry'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('donor')
    
    def urgency_badge(self, obj):
        urgency = obj.urgency_level
        days = obj.days_until_expiry
        
        color_map = {
            'critical': '#dc3545',  # Red
            'high': '#fd7e14',      # Orange
            'medium': '#ffc107',    # Yellow
            'low': '#28a745',       # Green
            'normal': '#6c757d',    # Gray
            'expired': '#343a40'    # Dark
        }
        
        color = color_map.get(urgency, '#6c757d')
        
        # Handle case when expiry_date is not set yet
        if days is None:
            text = "NO DATE SET"
        elif days < 0:
            text = f"EXPIRED ({abs(days)}d ago)"
        elif days == 0:
            text = "EXPIRES TODAY"
        elif days == 1:
            text = "EXPIRES TOMORROW"
        else:
            text = f"{urgency.upper()} ({days}d)"
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color, text
        )
    urgency_badge.short_description = 'Urgency'
    urgency_badge.admin_order_field = 'expiry_date'
    
    actions = ['mark_as_picked_up', 'mark_as_delivered', 'mark_as_cancelled']
    
    def mark_as_picked_up(self, request, queryset):
        updated = queryset.update(status=Donation.Status.PICKED_UP)
        self.message_user(request, f'{updated} donations marked as picked up.')
    mark_as_picked_up.short_description = "Mark selected donations as picked up"
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status=Donation.Status.DELIVERED)
        self.message_user(request, f'{updated} donations marked as delivered.')
    mark_as_delivered.short_description = "Mark selected donations as delivered"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status=Donation.Status.CANCELLED)
        self.message_user(request, f'{updated} donations marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected donations as cancelled"


admin.site.register(CustomUser, UserAdmin)
admin.site.register(GenericMedicine)
admin.site.register(BrandMedicine)


@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'recipient', 'quantity', 'urgency', 'status', 'tracking_code', 'created_at']
    list_filter = ['status', 'urgency', 'created_at']
    search_fields = ['medicine_name', 'tracking_code', 'recipient__email', 'recipient__first_name', 'recipient__last_name']
    readonly_fields = ['tracking_code', 'created_at', 'updated_at', 'days_since_request']
    fieldsets = (
        ('Request Information', {
            'fields': ('recipient', 'medicine_name', 'quantity', 'urgency', 'reason')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'tracking_code', 'matched_donation', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'days_since_request'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_matched', 'mark_as_fulfilled', 'mark_as_cancelled']
    
    def mark_as_matched(self, request, queryset):
        updated = queryset.update(status=MedicineRequest.Status.MATCHED)
        self.message_user(request, f'{updated} requests marked as matched.')
    mark_as_matched.short_description = "Mark selected as matched"
    
    def mark_as_fulfilled(self, request, queryset):
        updated = queryset.update(status=MedicineRequest.Status.FULFILLED)
        self.message_user(request, f'{updated} requests marked as fulfilled.')
    mark_as_fulfilled.short_description = "Mark selected as fulfilled"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status=MedicineRequest.Status.CANCELLED)
        self.message_user(request, f'{updated} requests marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected as cancelled"


# Customize admin site header
admin.site.site_header = "HealthBridge Administration"
admin.site.site_title = "HealthBridge Admin"
admin.site.index_title = "Welcome to HealthBridge Administration"