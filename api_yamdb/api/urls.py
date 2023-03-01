from rest_framework import routers
from django.urls import path, include

from .views import (
    # TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)


router_v1 = routers.DefaultRouter()

# router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='title-reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='title-review-comments')

urlpatterns = [
    path('', include(router_v1.urls)),
]
