from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('request/', views.request_medicine, name='request_medicine'),
    path('track/', views.track_medicine_requests, name='track_medicine_requests'),
    path('<int:pk>/', views.medicine_request_detail, name='medicine_request_detail'),
    path('<int:pk>/delete/', views.delete_medicine_request, name='delete_medicine_request'),
]
