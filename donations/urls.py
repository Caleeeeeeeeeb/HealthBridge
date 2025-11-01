from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('donate/', views.donate_medicine, name='donate_medicine'),
    path('my-donations/', views.my_donations, name='my_donations'),
    path('<int:pk>/', views.donation_detail, name='donation_detail'),
    path('delete/<int:donation_id>/', views.delete_donation, name='delete_donation'),
    path('search/', views.medicine_search, name='medicine_search'),
    path('api/autocomplete/', views.medicine_autocomplete, name='medicine_autocomplete'),
]
