from django.db import models
from django.utils.translation import ugettext_lazy as _

from users.models import User
from .constants import DESTINATION_CHOICES, EMAIL


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
    otp = models.CharField(verbose_name=_('OTP Code'), max_length=10)
    destination = models.CharField(
        verbose_name=_('Destination Address (Mobile/EMail)'),
        max_length=254,
        unique=True,
    )
    create_date = models.DateTimeField(verbose_name=_('Create Date'), auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=_('Date Modified'), auto_now=True)
    is_validated = models.BooleanField(verbose_name=_('Is Validated'), default=False)
    validate_attempt = models.IntegerField(
        verbose_name=_('Attempted Validation'),
        default=3,
    )
    prop = models.CharField(
        verbose_name=_('Destination Property'),
        default=EMAIL,
        max_length=3,
        choices=DESTINATION_CHOICES,
    )
    send_counter = models.IntegerField(verbose_name=_('OTP Sent Counter'), default=0)
    sms_id = models.CharField(
        verbose_name=_('SMS ID'),
        max_length=254,
        null=True,
        blank=True,
    )
    reactive_at = models.DateTimeField(verbose_name=_('ReActivate Sending OTP'))

    def __str__(self):
        return self.destination

    class Meta:
        verbose_name = _('OTP Validation')
        verbose_name_plural = _('OTP Validations')

