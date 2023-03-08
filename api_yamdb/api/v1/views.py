from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title

from .filters import TitleFilter
from .mixins import ModelViewSetWithoutPut, ModelViewSetWithoutRetrieve
from .permissions import (
    AdminOnly,
    AdminOnlyOrReadOnly,
    AuthorOrModeratorOrAdmin,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    TokenSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from .utils import send_confirmation_code

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    """Получить код подтверждения на указанный email"""
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get("email")
    username = serializer.validated_data.get("username")
    try:
        user, exist = User.objects.get_or_create(
            username=username, email=email
        )
    except Exception:
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    send_confirmation_code(email, confirmation_code)
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_token(request):
    """Получить токен для работы с API по коду подтверждения"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    confirmation_code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        message = {"confirmation_code": "Кот подтверждения неверен"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    message = {"token": AccessToken.for_user(user)}
    return Response(message, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSetWithoutPut):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(IsAuthenticated,),
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


class TitleViewSet(ModelViewSetWithoutPut):
    permission_classes = (AdminOnlyOrReadOnly,)
    queryset = Title.objects.all()
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleGetSerializer
        return TitlePostSerializer

    def get_queryset(self):
        queryset = Title.objects.all()
        if self.action in ("list", "retrieve"):
            queryset = Title.objects.annotate(rating=Avg("reviews__score"))
        return queryset


class CategoryViewSet(ModelViewSetWithoutRetrieve):
    permission_classes = (AdminOnlyOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreViewSet(ModelViewSetWithoutRetrieve):
    permission_classes = (AdminOnlyOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class ReviewViewSet(ModelViewSetWithoutPut):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, AuthorOrModeratorOrAdmin]

    def get_parent_title(self):
        return get_object_or_404(Title, pk=int(self.kwargs.get("title_id")))

    def get_queryset(self):
        title = self.get_parent_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_parent_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrModeratorOrAdmin)

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
