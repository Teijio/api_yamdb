from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Review,
    Comment,
)


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
