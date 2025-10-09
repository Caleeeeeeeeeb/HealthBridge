from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

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

    def save(self, *args, **kwargs):
        # create a short unique code like AB12CD34EF
        if not self.tracking_code:
            self.tracking_code = uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        base = f"{self.name} ({self.quantity})"
        return f"{base} • {self.get_status_display()}"
