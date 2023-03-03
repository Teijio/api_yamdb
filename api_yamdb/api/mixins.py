from rest_framework import mixins, viewsets
from rest_framework.viewsets import (
    GenericViewSet,
)


class CreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    pass


class ModelViewSetWithoutRetrieve(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass
