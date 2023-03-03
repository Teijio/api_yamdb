from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    TokenSerializer,
    UserCreateSerializer,
    UserSerializer,
    TitlePostSerializer,
    TitleGetSerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from reviews.models import (
    Title,
    Category,
    Genre,
)
from .mixins import (
    CreateViewSet,
    CreateListViewSet,
    ModelViewSetWithoutRetrieve,
)
from .utils import send_confirmation_code
from .permissions import (
    AdminOnly,
    AuthorOrModeratorOrAdmin,
    IsAuthor,
    ReadOnly,
)
from .filters import TitleFilter

User = get_user_model()


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
        AdminOnly,
    )
    filter_backends = [filters.SearchFilter]
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly | AdminOnly]
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleGetSerializer
        return TitlePostSerializer


class CategoryViewSet(ModelViewSetWithoutRetrieve):
    permission_classes = [ReadOnly | AdminOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)


class GenreViewSet(ModelViewSetWithoutRetrieve):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, AdminOnly]
        return [permission() for permission in permission_classes]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticated,
        AuthorOrModeratorOrAdmin,
    )

    def get_parent_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        title = self.get_parent_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_parent_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrAdmin,)

    def get_parent_review(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return get_object_or_404(
            title.reviews.all(), pk=self.kwargs.get("review_id")
        )

    def get_queryset(self):
        review = self.get_parent_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_parent_review()
        serializer.save(author=self.request.user, review=review)
