from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r"^[\w.@+-]+$", max_length=150)
    confirmation_code = serializers.CharField(max_length=150)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def validate_username(self, username):
        if username.lower() == "me":
            raise serializers.ValidationError("Использовать имя me запрещено")
        return username


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(regex=r"^[\w.@+-]+\Z", max_length=150)

    def validate_username(self, username):
        if username.lower() == "me":
            raise serializers.ValidationError("Использовать имя me запрещено")
        return username


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["id"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ["id"]


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для post-запросов модели Title."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )

    class Meta:
        model = Title
        fields = [
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        ]


class TitleGetSerializer(serializers.ModelSerializer):
    """Сериализатор для get-запросов модели Title."""

    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = [
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "pub_date"]

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    "Вы не можете повторно оставить рецензию."
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]
