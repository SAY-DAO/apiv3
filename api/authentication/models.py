from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User
from .constants import DESTINATION_CHOICES
from .constants import EMAIL


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
        return str(self.created_by.name) + ' | ' + str(self.created_by.username)

    class Meta:
        verbose_name = _('Authentication Transaction')
        verbose_name_plural = _('Authentication Transactions')


class OTPValidation(models.Model):
    otp = models.CharField(
        verbose_name=_('OTP Code'),
        max_length=10,
    )
    destination = models.CharField(
        verbose_name=_('Destination Address (Mobile/EMail)'),
        max_length=254,
        unique=True,
    )
    create_date = models.DateTimeField(verbose_name=_('Create Date'), auto_now_add=True)
    verify_date = models.DateTimeField(verbose_name=_('Date Verified'), auto_now=True)
    is_verified = models.BooleanField(verbose_name=_('Is Verified'), default=False)
    validate_attempt = models.IntegerField(
        verbose_name=_('Attempted Validation'),
        default=3,
    )
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
        return f'{self.destination} code: {self.otp}'

    class Meta:
        verbose_name = _('OTP Validation')
        verbose_name_plural = _('OTP Validations')

    @classmethod
    def import_from_v2(cls, *args):
        pass