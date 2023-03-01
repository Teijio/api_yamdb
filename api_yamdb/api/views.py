from rest_framework import permissions, status
from rest_framework.response import Response

from .serializers import TokenSerializer, UserCreateSerializer
from .mixins import CreateViewSet, CreateListViewSet
from .utils import generate_confirmation_code, send_confirmation_code
from users.models import User


class UserCreateViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = generate_confirmation_code()
        send_confirmation_code(
            email=user.email, confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class TokenReceiveViewSet(CreateViewSet):
    pass


class UserViewSet(CreateListViewSet):
    pass
