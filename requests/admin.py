from django.contrib import admin
from .models import MedicineRequest


@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'quantity', 'urgency', 'status', 'recipient', 'tracking_code', 'created_at']
    list_filter = ['status', 'urgency', 'created_at']
    search_fields = ['medicine_name', 'tracking_code', 'recipient__email']
    readonly_fields = ['tracking_code', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('medicine_name', 'quantity', 'urgency', 'reason', 'notes')
        }),
        ('Recipient Information', {
            'fields': ('recipient',)
        }),
        ('Status & Matching', {
            'fields': ('status', 'matched_donation', 'tracking_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
