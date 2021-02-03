from django.conf import settings
from django.utils.module_loading import import_string


def get_connection(backend=None, fail_silently=False, **kwds):
    """Load an sms backend and return an instance of it.

    If backend is None (default), use settings.SMS_BACKEND.

    Both fail_silently and other keyword arguments are used in the
    constructor of the backend.
    """
    klass = import_string(backend or settings.SMS_BACKEND)
    return klass(**kwds)


def send_sms(message, recipient,  connection=None):
    connection = connection or get_connection()
    connection.send(message, recipient)


def send_otp(message, recipient,  connection=None):
    """Has higher priority than normal sms, if backend support it"""

    connection = connection or get_connection()
    if hasattr(connection, 'send_otp') and callable(connection.send_otp):
        connection.send_otp(message, recipient)

    connection.send(message, recipient)  # fallback option

