from datetime import datetime, timedelta

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, AuthTransaction
from .serializers import LoginSerializer, UserSerializer
from .utils import get_client_ip


class LoginView(APIView):

    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def validated(self, serialized_data, *args, **kwargs):
        user = serialized_data.validated_data.get("user") or self.request.user
        token = serialized_data.validated_data.get("token")
        response_data = {
            'token': token,
            'user': UserSerializer(user,context={'request': self.request},).data
        }
        response = Response(response_data)
        # if api_settings.JWT_AUTH_COOKIE:
        expiration = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_DELTA)
        response.set_cookie(
            settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True
        )

        user.last_login = datetime.now()
        user.save()
        #
        AuthTransaction(
            created_by=user,
            token=token,
            ip_address=get_client_ip(self.request),
            session=user.get_session_auth_hash(),
        ).save()

        return response

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            return self.validated(serialized_data=serialized_data)
        else:
            return Response(
                serialized_data.errors,
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
