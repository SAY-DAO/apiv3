import pyotp
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User
from .constants import DESTINATION_CHOICES
from .constants import EMAIL, PHONE


class AuthTransaction(models.Model):
    ip_address = models.GenericIPAddressField(blank=False, null=False)
    token = models.TextField(verbose_name=_('JWT Token passed'))
    session = models.TextField(verbose_name=_('Session Passed'))
    create_date = models.DateTimeField(
        verbose_name=_('Create Date/Time'),
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        verbose_name=_('Date/Time Modified'),
        auto_now=True,
    )
    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.created_by.name} | {self.created_by.username}'

    class Meta:
        verbose_name = _('Authentication Transaction')
        verbose_name_plural = _('Authentication Transactions')


class OTPValidation(models.Model):
    destination = models.CharField(
        verbose_name=_('Destination Address (Mobile/EMail)'),
        max_length=254,
        unique=True,
    )
    create_date = models.DateTimeField(verbose_name=_('Create Date'), auto_now_add=True)
    verify_date = models.DateTimeField(verbose_name=_('Date Verified'))
    is_verified = models.BooleanField(verbose_name=_('Is Verified'), default=False)
    destination_type = models.CharField(
        verbose_name=_('Destination Type'),
        default=EMAIL,
        max_length=10,
        choices=DESTINATION_CHOICES,
    )
    secret = models.CharField(
        verbose_name=_('OTP Secret'),
        max_length=128,
    )
    send_counter = models.IntegerField(verbose_name=_('OTP Sent Counter'), default=0)

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
                    create_date=make_aware(v2_user.created),
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
                    create_date=make_aware(v2_user.created),
                    send_counter=1,
                    secret=pyotp.random_base32(),
                )
                otp.save()
