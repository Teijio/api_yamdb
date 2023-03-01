from django.urls import include, path
from rest_framework import routers

from .views import UserCreateViewSet, TokenReceiveViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
# router_v1.register(r"users", UserViewSet)

user_create = UserCreateViewSet.as_view({"post": "create"})
user_token = TokenReceiveViewSet.as_view({"post": "create"})

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", user_create, name="user-create"),
    path("v1/auth/token/", user_token, name="user-token"),
]
