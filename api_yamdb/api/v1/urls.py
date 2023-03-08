from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    get_confirmation_code,
    get_token,
)

router_v1 = routers.DefaultRouter()
router_v1.register(r"users", UserViewSet, basename="users")
router_v1.register(r"titles", TitleViewSet, basename="titles")
router_v1.register(r"categories", CategoryViewSet, basename="categories")
router_v1.register(r"genres", GenreViewSet, basename="genres")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="title-reviews",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="title-review-comments",
)

auth_urls = [
    path("signup/", get_confirmation_code, name="signup"),
    path("token/", get_token, name="token"),
]

urlpatterns = [
    path("auth/", include(auth_urls)),
    path("", include(router_v1.urls)),
]
