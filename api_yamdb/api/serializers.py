from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
# from rest_framework.response import Response

import re
import datetime

from reviews.models import (
    Title,
    Category,
    Genre,
    Review,
    Comment,
    GenreTitle,
)


User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        fields = ("username", "email")
        model = User

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Использовать имя me запрещено")
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)


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
        if username == "me":
            raise serializers.ValidationError("Использовать имя me запрещено")
        return username


class CategorySerializer(serializers.ModelSerializer):
    # name = serializers.CharField(required=True)
    # slug = serializers.CharField(required=True)

    class Meta:
        model = Category
        fields = ['name', 'slug']

    def validate_slug(self, value):
        if not re.match(r"^[-a-zA-Z0-9_]+$", value) or len(value) > 50:
            raise serializers.ValidationError(
                "Поле slug не соответствует паттерну")
        return value

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                "Поле name длиннее 256 символов")
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']

    def validate_slug(self, value):
        if not re.match(r"^[-a-zA-Z0-9_]+$", value) or len(value) > 50:
            raise serializers.ValidationError(
                "Поле slug не соответствует паттерну")
        return value

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                "Поле name длиннее 256 символов")
        return value


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'year',
                  'rating', 'description', 'genre', 'category']

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            raise serializers.ValidationError("Поле genre не найдено")
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(Genre, slug=genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title

    def get_rating(self, instance):
        if instance.reviews.count() == 0:
            return None
        return int(round(
            number=instance.reviews.aggregate(Avg('score'))['score__avg'],
            ndigits=0
        ))

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                "Поле name длиннее 256 символов")
        return value

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                "Указанный год еще не наступил")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    text = serializers.CharField(required=True)
    author = serializers.SlugRelatedField(slug_field="author", read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=["author", "title"]
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    text = serializers.CharField(required=True)
    author = serializers.SlugRelatedField(slug_field="author", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
