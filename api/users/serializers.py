from rest_framework import serializers

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
            'last_login'
        )
        read_only_fields = ('is_superuser', 'is_staff', 'last_login')
        extra_kwargs = {'password': {'write_only': True}}
