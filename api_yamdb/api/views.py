from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


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
        confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=user.email, confirmation_code=confirmation_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenReceiveViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                "Пользователь не найден", status=status.HTTP_404_NOT_FOUND
            )
        if not default_token_generator.check_token(user, confirmation_code):
            message = {"confirmation_code": "Кот подтверждения неверен"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {"token": str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(CreateListViewSet):
    pass
