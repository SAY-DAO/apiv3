from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AuthTransaction
from .serializers import LoginSerializer
from .utils import get_client_ip


class LoginView(APIView):

    serializer_class = LoginSerializer
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

