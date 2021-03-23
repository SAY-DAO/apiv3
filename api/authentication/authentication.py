from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from authentication.blacklist import is_token_blacklisted


class BlacklistJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)

        if is_token_blacklisted(token['jti']):
            raise InvalidToken({
                'detail':   _('Given token blacklisted'),
            })

        return token
