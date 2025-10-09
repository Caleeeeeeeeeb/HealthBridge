from django.urls import path
from . import views
from django.conf import settings  # 🆕 For accessing MEDIA_URL and MEDIA_ROOT
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), 
    path('search/', views.medicine_search, name='medicine_search'),
    path('donate/', views.donate_medicine, name='donate_medicine'),
]

# 🆕 This enables Django to display uploaded images in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
