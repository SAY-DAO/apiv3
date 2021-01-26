from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.text import gettext_lazy as _

from .models import AuthTransaction
from .models import OTPValidation
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


class OTPValidationAdmin(admin.ModelAdmin):
    """OTP Validation Admin"""

    list_display = ("destination", "otp", "prop")


class AuthTransactionAdmin(admin.ModelAdmin):
    """AuthTransaction Admin"""

    list_display = ("created_by", "ip_address", "create_date")

    def has_add_permission(self, request):
        """Limits admin to add an object."""

        return False

    def has_change_permission(self, request, obj=None):
        """Limits admin to change an object."""

        return False

    def has_delete_permission(self, request, obj=None):
        """Limits admin to delete an object."""

        return False


admin.site.register(User, DRFUserAdmin)
admin.site.register(OTPValidation, OTPValidationAdmin)
admin.site.register(AuthTransaction, AuthTransactionAdmin)