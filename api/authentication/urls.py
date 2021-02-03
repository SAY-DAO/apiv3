from django.urls import path


from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('otp/', views.OTPView.as_view(), name='otp'),
    path('otp/verify/', views.VerifyOTPView.as_view(), name='verify_otp'),
]

