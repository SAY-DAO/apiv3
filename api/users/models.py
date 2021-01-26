from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .constants import EMAIL, DESTINATION_CHOICES
from .managers import UserManager


class User(AbstractUser):
    username_regex = RegexValidator(
        regex=r'[A-Za-z0-9][.A-Za-z0-9]{3,11}$',
        message='username must start with letter and can have dot in it, must be 4 to 12 characters length',
    )
    username = models.CharField(
        validators=[username_regex],
        blank=False,
        null=False,
        unique=True,
        max_length=12,
    )

    normalized_username = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=12,
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.',
    )
    phone = models.CharField(
        validators=[phone_regex],
        blank=True,
        null=True,
        unique=True,
        max_length=15,
    )
    is_phone_verified = models.BooleanField(default=False)

    email = models.EmailField(blank=True)
    is_email_verified = models.BooleanField(default=False, null=True)

    objects = UserManager()


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