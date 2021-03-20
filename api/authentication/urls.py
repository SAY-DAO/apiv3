from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'register', views.RegisterViewSet, basename='register')

app_name = 'authentication'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('otp/', views.OTPView.as_view(), name='otp'),
    path('otp/verify/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('reset-password/', views.ResetPaswordView.as_view(), name='reset-password'),
    path('reset-password/confirm', views.ConfirmResetPaswordView.as_view(), name='confirm-reset-password'),
]

urlpatterns += router.urls
