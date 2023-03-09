import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            ("%(value)s год не должен быть больше текущего."),
            params={"value": value},
        )
