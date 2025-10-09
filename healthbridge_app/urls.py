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

    path("search/", views.medicine_search, name="medicine_search"),
    path("donate/", views.donate_medicine, name="donate_medicine"),

    # tracking
    path("requests/", views.my_donations, name="request_list"),
    path("requests/<int:pk>/", views.donation_detail, name="request_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
