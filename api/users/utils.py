
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
