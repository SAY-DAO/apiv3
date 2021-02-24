import email_normalize
from django.db.models import Q
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.get_or_none import get_or_none
from users.models import User
from users.utils import make_password
from . import models
from .utils import get_tokens_for_user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, write_only=True)
    password = serializers.CharField(max_length=200, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        handle = attrs['username']

        possible_email = ''
        try:
            possible_email = email_normalize.normalize(handle).normalized_address
        except ValueError:
            pass

        user = get_or_none(
            User,
            Q(
                Q(slug_username=slugify(handle))
                | (Q(normalized_email=possible_email) & Q(is_email_verified=True))
                | (Q(phone=handle) & Q(is_phone_verified=True))
            ),
        )

        if user is None:
            raise serializers.ValidationError(_('Invalid username or password'))

        if not user.check_password(attrs['password']):
            raise serializers.ValidationError(_('Invalid username or password'))

        if not user.is_active:
            raise serializers.ValidationError(_('Confirm email or password`'))

        self.user = user
        return get_tokens_for_user(user)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError(_('one of email or phone must is requeired'))

        if data.get('email'):
            if not get_or_none(
                models.OTPValidation,
                destination=data['email'],
                is_verified=True,
            ):
                raise serializers.ValidationError({'email': _('email is not verified')})

            data['is_email_verified'] = True

        if data.get('phone'):
            if not get_or_none(
                models.OTPValidation,
                destination=data['phone'],
                is_verified=True,
            ):
                raise serializers.ValidationError({'phone': _('phone is not verified')})

            data['is_phone_verified'] = True

        data['password'] = make_password(data['password'])
        return data


class OTPSerializer(serializers.Serializer):
    destination = serializers.CharField(max_length=200)
    send_counter = serializers.IntegerField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            normalized_email = email_normalize.normalize(attrs['destination'])
            validated_data['destination'] = normalized_email.normalized_address
        except ValueError:
            pass

        return validated_data


class VerifyOTPSerializer(OTPSerializer):
    otp = serializers.CharField(max_length=10, write_only=True)
