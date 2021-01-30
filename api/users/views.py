from rest_framework import viewsets, mixins, permissions

from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets, mixins, permissions

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
