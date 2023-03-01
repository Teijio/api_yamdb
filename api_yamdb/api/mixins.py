from rest_framework import mixins
from rest_framework.viewsets import (
    GenericViewSet,
)


class CreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    pass
