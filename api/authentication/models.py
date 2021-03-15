from urllib.parse import urljoin

import pyotp
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from common.mixins.timestamp import TimestampMixin
from users.models import User
from .constants import DESTINATION_CHOICES
from .constants import EMAIL
from .constants import PHONE
from common.sms import send_sms


class AuthTransaction(models.Model, TimestampMixin):
    ip_address = models.GenericIPAddressField(blank=False, null=False)
    session = models.TextField(verbose_name=_('Session Passed'))
    token = models.TextField(verbose_name=_('JWT Token passed'))

    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.created_by.name} | {self.created_by.username}'

    class Meta:
        verbose_name = _('Authentication Transaction')
        verbose_name_plural = _('Authentication Transactions')


class OTPValidation(models.Model, TimestampMixin):
    created_at = models.DateTimeField(verbose_name=_('Create Date'), auto_now_add=True)
    destination = models.CharField(
        verbose_name=_('Destination Address (Mobile/EMail)'),
        max_length=254,
        unique=True,
    )
    destination_type = models.CharField(
        verbose_name=_('Destination Type'),
        default=EMAIL,
        max_length=10,
        choices=DESTINATION_CHOICES,
    )
    is_verified = models.BooleanField(verbose_name=_('Is Verified'), default=False)
    secret = models.CharField(
        verbose_name=_('OTP Secret'),
        max_length=128,
    )
    send_counter = models.IntegerField(verbose_name=_('OTP Sent Counter'), default=0)
    verify_date = models.DateTimeField(verbose_name=_('Date Verified'), null=True)

    def __str__(self):
        return f'{self.destination} otp'

    class Meta:
        verbose_name = _('OTP Validation')
        verbose_name_plural = _('OTP Validations')

    def is_valid(self, code):
        totp = pyotp.TOTP(
            self.secret,
            digits=settings.OTP_DIGITS,
            interval=settings.OTP_LIFETIME,
        )
        return totp.verify(code)

    @classmethod
    def import_from_v2(cls, *args):
        from v2 import models as v2_models
        from django.utils.timezone import make_aware
        v2_user: v2_models.User

        for v2_user in v2_models.User.objects.all():
            if v2_user.is_email_verified:
                otp = cls(
                    destination=v2_user.emailaddress,
                    is_verified=True,
                    destination_type=EMAIL,
                    verify_date=make_aware(v2_user.created),
                    created_at=make_aware(v2_user.created),
                    send_counter=1,
                    secret=pyotp.random_base32(),
                )
                otp.save()

            if v2_user.is_phonenumber_verified:
                otp = cls(
                    destination=v2_user.phone_number,
                    is_verified=True,
                    destination_type=PHONE,
                    verify_date=make_aware(v2_user.created),
                    created_at=make_aware(v2_user.created),
                    send_counter=1,
                    secret=pyotp.random_base32(),
                )
                otp.save()


class ResetPassword(models.Model, TimestampMixin):
    token = models.CharField(max_length=10, unique=True)
    destination = models.CharField(
        verbose_name=_('Destination Address (Mobile/EMail)'),
        max_length=254,
        unique=True,
    )
    destination_type = models.CharField(
        verbose_name=_('Destination Type'),
        default=EMAIL,
        max_length=10,
        choices=DESTINATION_CHOICES,
    )

    @property
    def link(self):
        return urljoin(
            settings.BASE_URL,
            settings.SET_PASSWORD_URL + f'?token={self.token}'
        )

    def send_email(self):
        # Fix i18n
        send_mail(
            _('SAY Change Password'),
            render_to_string('reset_password.html', {'link': self.link}),
            recepiant_list=[self.destination],
            fail_silently=False,
        )

    def send_sms(self):
        send_sms(
            self.destination,
            _('Click on the link below to change your password.\n%s') % self.link
        )
