from django.utils.translation import gettext_lazy as _


def email_normalizer(email: str) -> str:
    try:
        # remove spaces at start and end of the and lowercase email address
        email = email.strip().lower()

        # split email into username and domain information
        username, domain = email.split('@')

        # remove . characters from username
        username = username.replace('.', '')

        # remove everything after +
        username = username.split('+')[0]
    except (AttributeError):
        raise ValueError(_('Invalid email address'))

    return f'{username}@{domain}'
