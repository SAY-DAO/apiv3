from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampMixin:
    created_at = models.DateTimeField(
        verbose_name=_('Create Date/Time'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Date/Time Modified'),
        auto_now=True,
    )
