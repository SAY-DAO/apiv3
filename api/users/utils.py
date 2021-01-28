import os
from hashlib import sha256

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
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def make_password(password):
    """
    v2 password hashing
        password: 64 bit hasshed + 64 bit salt
    """

    password = str(password)
    salt = sha256()
    salt.update(os.urandom(60))
    salt = salt.hexdigest()

    hashed_pass = sha256()
    # Make sure password is a str because we cannot hash unicode objects
    hashed_pass.update((password + salt).encode('utf-8'))
    hashed_pass = hashed_pass.hexdigest()

    password = salt + hashed_pass
    return password


def check_password(hashed_password, raw_password):
    """ v2 password checking """

    hashed_pass = sha256()
    hashed_pass.update((raw_password + hashed_password[:64]).encode('utf-8'))
    return hashed_password[64:] == hashed_pass.hexdigest()

