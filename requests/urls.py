from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('create/', views.create_request, name='create_request'),
    path('request/', views.request_medicine, name='request_medicine'),
    path('track/', views.track_medicine_requests, name='track_medicine_requests'),
    path('<int:pk>/', views.medicine_request_detail, name='medicine_request_detail'),
    path('<int:pk>/delete/', views.delete_medicine_request, name='delete_medicine_request'),
    path('<int:pk>/deliver/', views.deliver_medicine, name='deliver_medicine'),
    path('<int:pk>/claim/', views.claim_medicine, name='claim_medicine'),
]
