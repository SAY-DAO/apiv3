from datetime import datetime

from rest_framework import status, viewsets, mixins, permissions
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AuthTransaction, User
from .serializers import LoginSerializer, UserSerializer
from .utils import get_client_ip, get_tokens_for_user


class LoginView(APIView):

    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def validated(self, serialized_data, *args, **kwargs):
        user = serialized_data.validated_data.get("user") or self.request.user
        tokens = get_tokens_for_user(user)
        response = Response(tokens)

        user.last_login = datetime.now()
        user.save()

        AuthTransaction(
            created_by=user,
            token=tokens['access'],
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


class UserViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
