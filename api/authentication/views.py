import pyotp
from django.conf import settings
from django.core import exceptions
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

from common.sms import send_sms
from users.models import User
from . import serializers
from .constants import EMAIL
from .constants import PHONE
from .models import AuthTransaction
from .models import OTPValidation
from .utils import generate_otp
from .utils import get_client_ip


class LoginView(views.APIView):

    serializer_class = serializers.LoginSerializer
    permission_classes = ()
    authentication_classes = ()

    def validated(self, serialized_data, *args, **kwargs):
        user = serialized_data.user
        user.last_login = datetime.utcnow()
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
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
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
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
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
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY
                    )

            secret = pyotp.random_base32()
            otp = OTPValidation(
                secret=secret,
                destination=destination,
                destination_type=destination_type,
            )

        otp.send_counter += 1
        otp.save()

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

        return Response(_('Verification sent to %(destination)s.' % {'destination': destination}))


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
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        destination = serialized_data.validated_data['destination']
        code = serialized_data.validated_data['otp']

        try:
            otp = OTPValidation.objects.get(destination=destination)
        except OTPValidation.DoesNotExists:
            return Response(
                {'destination': _('destination is not a valid email/phone.')},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if not otp.is_valid(code):
            return Response(
                {'code': _('OTP code is invalid.')},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        otp.is_verified = True
        otp.verified_date = datetime.utcnow()
        otp.save()

        return Response(_('%(destination)s verified.' % {'destination': destination}))
