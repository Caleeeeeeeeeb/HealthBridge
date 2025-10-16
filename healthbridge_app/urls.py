from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),

    # API endpoints
    path("api/medicine-autocomplete/", views.medicine_autocomplete, name="medicine_autocomplete"),

    path("search/", views.medicine_search, name="medicine_search"),
    path("donate/", views.donate_medicine, name="donate_medicine"),

    # Donor tracking
    path("requests/", views.my_donations, name="request_list"),
    path("requests/<int:pk>/", views.donation_detail, name="request_detail"),
    path("donations/<int:pk>/delete/", views.delete_donation, name="delete_donation"),
    
    # Recipient features
    path("recipient/", views.recipient_dashboard, name="recipient_dashboard"),
    path("recipient/request/", views.request_medicine, name="request_medicine"),
    path("recipient/track/", views.track_medicine_requests, name="track_medicine_requests"),
    path("recipient/track/<int:pk>/", views.medicine_request_detail, name="medicine_request_detail"),
    path("recipient/requests/<int:pk>/delete/", views.delete_medicine_request, name="delete_medicine_request"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
