from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.text import gettext_lazy as _

from .models import User


class DRFUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "normalized_username")}),
        (_("Personal info"), {"fields": ("email", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "phone", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "phone", "is_staff")
    search_fields = ("username", "email", "phone")
    readonly_fields = ("date_joined", "last_login")


admin.site.register(User, DRFUserAdmin)
