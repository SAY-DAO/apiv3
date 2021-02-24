import email_normalize
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

from .managers import UserManager
from .utils import check_password
from .utils import make_password


class User(AbstractUser):
    username_regex = RegexValidator(
        regex=r'[A-Za-z0-9][.A-Za-z0-9]{3,21}$',
        message='username must start with letter and can have dot in it, must be 4 to 22 characters length',
    )
    username = models.CharField(
        validators=[username_regex],
        blank=False,
        null=False,
        unique=True,
        max_length=22,
    )
    slug_username = models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=22,
    )

    phone_regex = RegexValidator(
        regex=r'^\+\d{9,15}$',
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

    email = models.EmailField(blank=True, null=True, unique=True)
    normalized_email = models.EmailField(blank=True, null=True, unique=True)
    is_email_verified = models.BooleanField(default=False, null=True)

    objects = UserManager()

    # overwriting to be backward compatible with v2
    def check_password(self, raw_password):
        return check_password(self.password, raw_password)

    # overwriting to be backward compatible with v2
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def save(self, *args, **kwargs):
        self.slug_username = slugify(self.username)

        try:
            self.normalized_email = email_normalize.normalize(self.email).normalized_address
        except ValueError:
            pass

        super().save(*args, **kwargs)

    @classmethod
    def import_from_v2(cls, *args):
        from v2 import models as v2_models
        from django.utils.timezone import make_aware

        for v2_user in v2_models.User.objects.all():
            user = cls()
            user.id = v2_user.id
            user.username = v2_user.username
            user.slug_username = v2_user.username.lower()
            user.phone = v2_user.phone_number
            user.is_phone_verified = v2_user.is_phonenumber_verified
            user.email = v2_user.emailaddress
            user.normalized_email = email_normalize.normalize(v2_user.emailaddress).normalized_address
            user.is_email_verified = v2_user.is_email_verified
            user.password = v2_user.field_password
            user.first_name = v2_user.firstname
            user.last_name = v2_user.lastname
            user.last_login = make_aware(v2_user.lastlogin)
            user.date_joined = make_aware(v2_user.created)
            user.is_active = True
            user.save()

