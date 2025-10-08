from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import CustomUser, GenericMedicine, BrandMedicine, Donation

admin.site.register(CustomUser, UserAdmin)
admin.site.register(GenericMedicine)
admin.site.register(BrandMedicine)
admin.site.register(Donation)