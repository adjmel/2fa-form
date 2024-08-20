from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from .views import verify_2fa

urlpatterns = [
    path('', views.user_login, name='login'),
    path('enable_2fa/', views.enable_2fa, name='enable_2fa'),
    path('verify_2fa/', views.verify_2fa, name='verify_2fa'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('success_page/', views.success_page, name='success_page'),
]
