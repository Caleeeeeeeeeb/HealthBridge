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
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()
   
    
    # 🆕 Added field to store uploaded medicine image
    image = models.ImageField(upload_to='donations/', null=True, blank=True)
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"