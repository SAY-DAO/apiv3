import pyotp
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


def get_client_ip(request):
    """
    Fetches the IP address of a client from Request and
    return in proper format.
    Source: https://stackoverflow.com/a/4581997
    Parameters
    ----------
    request: django.http.HttpRequest
    Returns
    -------
    ip: str
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': f'Bearer {refresh.access_token}',
    }


def generate_otp(secret):
    return pyotp.TOTP(
        secret,
        digits=settings.OTP_DIGITS,
        interval=settings.OTP_LIFETIME,
    ).now()
