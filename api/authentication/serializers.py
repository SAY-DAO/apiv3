from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from users.models import User
from .models import OTPValidation
from .utils import get_tokens_for_user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, write_only=True)
    password = serializers.CharField(max_length=200, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(normalized_username=attrs['username'].lower())
        except User.DoesNotExist:
            raise serializers.ValidationError(_('Invalid username or password'))

        if not user.check_password(attrs['password']):
            raise serializers.ValidationError(_('Invalid username or password'))

        if not user.is_active:
            raise serializers.ValidationError(_('Confirm email or password`'))

        self.user = user
        return get_tokens_for_user(user)


class OTPSerializer(serializers.Serializer):
    destination = serializers.CharField(max_length=15, write_only=True)


class VerifyOTPSerializer(serializers.Serializer):
    destination = serializers.CharField(max_length=15, write_only=True)
    otp = serializers.CharField(max_length=10, write_only=True)
