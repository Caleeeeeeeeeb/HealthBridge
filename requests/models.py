from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


class MedicineRequest(models.Model):
    """Model for recipients to request medicines"""
    
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        MATCHED = "matched", "Matched"
        FULFILLED = "fulfilled", "Fulfilled"
        CLAIMED = "claimed", "Claimed"
        CANCELLED = "cancelled", "Cancelled"
    
    class Urgency(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"
    
    # Request details - matching database column names
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medicine_requests",
        db_column="recipient_id"
    )
    medicine_name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)  # varchar in DB
    urgency = models.CharField(
        max_length=10,
        choices=Urgency.choices,
        default=Urgency.MEDIUM
    )
    reason = models.TextField(blank=True, help_text="Why do you need this medicine?")
    notes = models.TextField(blank=True, default="")
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    tracking_code = models.CharField(max_length=12, unique=True, editable=False)
    
    # Matching
    matched_donation = models.ForeignKey(
        'donations.Donation',  # Reference to donations app
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="matched_requests",
        db_column="matched_donation_id"
    )
    
    # Timestamps - matching database column names
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        db_table = 'healthbridge_app_medicinerequest'
    
    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = f"REQ{uuid4().hex[:9].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def quantity_needed(self):
        """Alias for quantity to maintain compatibility"""
        try:
            return int(self.quantity)
        except (ValueError, TypeError):
            return 0
    
    @property
    def requester(self):
        """Alias for recipient to maintain compatibility"""
        return self.recipient
    
    @property
    def days_since_request(self):
        """Calculate days since request was made"""
        delta = timezone.now() - self.created_at
        return delta.days
    
    def __str__(self):
        return f"{self.medicine_name} - {self.get_status_display()} ({self.tracking_code})"
