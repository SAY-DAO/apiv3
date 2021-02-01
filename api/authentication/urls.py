from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'authentication'

router = DefaultRouter()
router.register(r'otp/verify', views.VerifyOTPViewSet, basename='verify_otp')

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('otp/', views.OTPView.as_view(), name='otp'),
]

urlpatterns += router.urls
