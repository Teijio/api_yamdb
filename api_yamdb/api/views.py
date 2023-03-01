from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view

from .serializers import TokenSerializer, UserCreateSerializer
from .mixins import CreateViewSet
from users.models import User

class UserCreateViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)
