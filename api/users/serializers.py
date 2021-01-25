from django.contrib.auth import login
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone',
            'password',
            'is_superuser',
            'is_staff',
        )
        read_only_fields = ('is_superuser', 'is_staff')
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(normalized_username=attrs['username'].lower())
        except User.DoesNotExist:
            raise serializers.ValidationError(_('Invalid username or password'))

        if not user.check_password(attrs['password']):
            raise serializers.ValidationError(_('Invalid username or password'))

        if not user.is_active:
            raise serializers.ValidationError(_('Confirm email or password`'))

        return {
            'token': 1,
            'user': user
        }
