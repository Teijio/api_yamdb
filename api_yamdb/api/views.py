from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from reviews.models import (
    Title,
    # Review,
    # Comment,
)
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    # permission_classes = []

    def get_parent_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        title = self.get_parent_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_parent_title()
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    # permission_classes = []

    def get_parent_review(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return get_object_or_404(
            title.reviews.all(),
            pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        review = self.get_parent_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_parent_review()
        serializer.save(
            author=self.request.user,
            review=review
        )
