from uuid import uuid4
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class GenericMedicine(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BrandMedicine(models.Model):
    brand_name = models.CharField(max_length=100)
    generic = models.ForeignKey(GenericMedicine, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return f"{self.brand_name} ({self.generic.name})"


class DonationManager(models.Manager):
    """Custom manager for Donation model with expiry-related methods"""
    
    def expiring_within(self, days=10):
        """Get donations expiring within specified days"""
        target_date = date.today() + timedelta(days=days)
        return self.filter(
            expiry_date__lte=target_date,
            expiry_date__gte=date.today(),
            status__in=[Donation.Status.AVAILABLE, Donation.Status.RESERVED]
        )
    
    def expired(self):
        """Get expired donations"""
        return self.filter(expiry_date__lt=date.today())
    
    def critical_expiry(self):
        """Get donations expiring today or tomorrow"""
        return self.expiring_within(days=1)
    
    def by_urgency(self):
        """Order donations by expiry urgency"""
        return self.filter(
            expiry_date__gte=date.today(),
            status__in=[Donation.Status.AVAILABLE, Donation.Status.RESERVED]
        ).order_by('expiry_date')


class Donation(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        RESERVED = "reserved", "Reserved"
        PICKED_UP = "picked_up", "Picked up"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    # core data
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()

    # who donated (optional – but enables tracking per user)
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="donations",
    )

    # image + tracking fields
    image = models.ImageField(upload_to='donations/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    tracking_code = models.CharField(max_length=12, unique=True, editable=False)
    donated_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, default="")

    objects = DonationManager()  # Custom manager

    def save(self, *args, **kwargs):
        # create a short unique code like AB12CD34EF
        if not self.tracking_code:
            self.tracking_code = uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    @property
    def days_until_expiry(self):
        """Calculate days until expiry (negative if already expired)"""
        if not self.expiry_date:
            return None
        delta = self.expiry_date - date.today()
        return delta.days
    
    @property
    def is_expiring_soon(self, days_threshold=10):
        """Check if medicine is expiring within threshold days"""
        if not self.expiry_date:
            return False
        days = self.days_until_expiry
        return days is not None and 0 <= days <= days_threshold
    
    @property
    def is_expired(self):
        """Check if medicine has already expired"""
        if not self.expiry_date:
            return False
        return self.expiry_date < date.today()
    
    @property
    def urgency_level(self):
        """Return urgency level based on days until expiry"""
        if not self.expiry_date:
            return "normal"
        
        days = self.days_until_expiry
        if days is None:
            return "normal"
        elif days < 0:
            return "expired"
        elif days == 0:
            return "critical"  # expires today
        elif days <= 3:
            return "high"      # expires in 1-3 days
        elif days <= 7:
            return "medium"    # expires in 4-7 days
        elif days <= 14:
            return "low"       # expires in 8-14 days
        else:
            return "normal"    # expires in 15+ days

    def __str__(self):
        base = f"{self.name} ({self.quantity})"
        return f"{base} • {self.get_status_display()}"


class ExpiryAlert(models.Model):
    """Track expiry notifications sent to avoid duplicates"""
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='expiry_alerts')
    alert_sent_at = models.DateTimeField(auto_now_add=True)
    days_before_expiry = models.PositiveIntegerField()
    recipient_email = models.EmailField()
    alert_type = models.CharField(
        max_length=20,
        choices=[
            ('email', 'Email'),
            ('dashboard', 'Dashboard'),
            ('sms', 'SMS'),  # Future feature
        ],
        default='email'
    )
    
    class Meta:
        unique_together = ['donation', 'days_before_expiry', 'recipient_email']
        ordering = ['-alert_sent_at']
    
    @property
    def was_sent_recently(self):
        """Check if alert was sent in the last 24 hours"""
        return self.alert_sent_at >= timezone.now() - timedelta(days=1)
    
    def __str__(self):
        return f"Alert for {self.donation.name} ({self.days_before_expiry} days before expiry)"


class MedicineRequest(models.Model):
    """Model for recipients to request medicines"""
    
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        MATCHED = "matched", "Matched"
        FULFILLED = "fulfilled", "Fulfilled"
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
        Donation,
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
