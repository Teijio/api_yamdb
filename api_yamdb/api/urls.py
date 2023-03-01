from django.urls import include, path

from rest_framework import routers

router_v1 = routers.DefaultRouter()
# router_v1.register(r"users", UserViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/signup/", include(router_v1.urls)),
    path("v1/token/", include(router_v1.urls)),
]