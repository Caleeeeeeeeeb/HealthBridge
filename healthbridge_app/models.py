from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=120)
    uses = models.CharField(max_length=255, blank=True)
    form = models.CharField(max_length=60, blank=True)
    expiry = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='medicines/', null=True, blank=True)  # uploadable
    image_url = models.URLField(blank=True)  # external URL or leave empty

    def __str__(self):
        return self.name
