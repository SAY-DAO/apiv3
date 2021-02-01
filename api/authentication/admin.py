from django.contrib import admin

from .models import AuthTransaction
from .models import OTPValidation


class OTPValidationAdmin(admin.ModelAdmin):
    """OTP Validation Admin"""

    list_display = ("destination", "otp", "destination_type")


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


admin.site.register(OTPValidation, OTPValidationAdmin)
admin.site.register(AuthTransaction, AuthTransactionAdmin)