from rest_framework import mixins, serializers
from rest_framework.viewsets import (
    GenericViewSet,
)

import re
import datetime


class CreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    pass


class NameValidationMixin():
    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                "Поле name длиннее 256 символов")
        return value


class SlugValidationMixin():
    def validate_slug(self, value):
        if not re.match(r"^[-a-zA-Z0-9_]+$", value) or len(value) > 50:
            raise serializers.ValidationError(
                "Поле slug не соответствует паттерну")
        return value


class YearValidationMixin():
    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                "Указанный год еще не наступил")
        return value
