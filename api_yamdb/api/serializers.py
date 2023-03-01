from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Review,
    Comment,
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
 

class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    author = serializers.SlugRelatedField(
        slug_field='author',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        # Согласно ТЗ необходимо, чтобы соблюдалось условие:
        # == "1 отзыв для 1 произведения от 1 автора" ==
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='author',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
