import secrets

import pyotp
from django.conf import settings
from django.core import exceptions
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

from common.get_or_none import get_or_none
from common.sms import send_sms
from users.models import User
from . import serializers
from .constants import EMAIL
from .constants import PHONE
from .models import AuthTransaction
from .models import OTPValidation
from .models import ResetPassword
from .utils import generate_otp
from .utils import get_client_ip


class LoginView(views.APIView):

    serializer_class = serializers.LoginSerializer
    permission_classes = ()
    authentication_classes = ()

    def validated(self, serialized_data, *args, **kwargs):
        user = serialized_data.user
        user.last_login = timezone.now()
        user.save()

        AuthTransaction(
            created_by=user,
            token=serialized_data.data['access'],
            ip_address=get_client_ip(self.request),
            session=user.get_session_auth_hash(),
        ).save()

        return Response(serialized_data.data)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            return self.validated(serialized_data=serialized_data)
        else:
            return Response(
                serialized_data.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class OTPView(views.APIView):
    serializer_class = serializers.OTPSerializer
    permission_classes = ()
    authentication_classes = ()
    throttle_scope = 'send_otp'

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)

        if not serialized_data.is_valid():
            return Response(
                serialized_data.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        destination = serialized_data.validated_data['destination']

        try:
            otp = OTPValidation.objects.get(destination=destination)
        except OTPValidation.DoesNotExist:
            try:
                validate_email(destination)
                destination_type = EMAIL
            except exceptions.ValidationError:
                try:
                    User.phone_regex(destination)
                    destination_type = PHONE
                except exceptions.ValidationError:
                    return Response(
                        {'destination': _('destination is not a valid email/phone.')},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            secret = pyotp.random_base32()
            otp = OTPValidation(
                secret=secret,
                destination=destination,
                destination_type=destination_type,
            )

        code = generate_otp(otp.secret)

        if otp.destination_type == EMAIL:
            send_mail(
                _('SAY Email Verification'),
                _('SAY Email Verification: %(code)s' % {'code': code}),
                settings.VERIFICATION_EMAIL_FROM,
                [otp.destination],
                fail_silently=False,
            )
        else:
            send_sms(
                _('SAY verification code: %(code)s' % {'code': code}),
                otp.destination,
            )

        otp.send_counter += 1
        otp.save()

        return Response(serializers.OTPSerializer(otp).data)


class VerifyOTPView(views.APIView):
    serializer_class = serializers.VerifyOTPSerializer
    permission_classes = ()
    authentication_classes = ()
    throttle_scope = 'verify_otp'

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)

        if not serialized_data.is_valid():
            return Response(
                serialized_data.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        destination = serialized_data.validated_data['destination']
        code = serialized_data.validated_data['otp']

        try:
            otp = OTPValidation.objects.get(destination=destination)
        except OTPValidation.DoesNotExists:
            return Response(
                {'destination': _('destination is not a valid email/phone.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not otp.is_valid(code):
            return Response(
                {'code': _('OTP code is invalid.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp.is_verified = True
        otp.verified_date = datetime.utcnow()
        otp.save()

        return Response(serializers.OTPSerializer(otp).data)


class RegisterViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.RegisterSerializer
    permission_classes = ()
    authentication_classes = ()


class ResetPaswordView(views.APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.ResetPasswordSerializer
    throttle_scope = 'request_reset_password'

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)

        if not serialized_data.is_valid():
            return Response(
                serialized_data.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        destination = serialized_data.validated_data['destination']
        reset_password = ResetPassword(
            destination=destination,
            token=secrets.token_urlsafe()[:settings.RESET_PASSWORD_TOKEN_LENGTH],
        )

        try:
            validate_email(destination)
            reset_password.destination_type = EMAIL
        except exceptions.ValidationError:
            try:
                User.phone_regex(destination)
                reset_password.destination_type = PHONE
            except exceptions.ValidationError:
                return Response(
                    {'destination': _('destination is not a valid email/phone.')},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if reset_password.destination_type == EMAIL:
            user = get_or_none(User, email=reset_password.destination)
        else:
            user = get_or_none(User, phone=reset_password.destination)

        if user is None:
            return Response(
                {'destination': _('destination not found.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reset_password.user = user
        reset_password.save()
        return Response(serializers.ResetPasswordSerializer(reset_password).data)


class ConfirmResetPaswordView(views.APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.ConfirmResetPasswordSerializer
    throttle_scope = 'confirm_reset_password'

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if not serialized_data.is_valid():
            return Response(
                serialized_data.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response()
