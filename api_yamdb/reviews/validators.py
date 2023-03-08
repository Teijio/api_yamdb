import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            ("%(value)s проверьте год произведения"),
            params={"value": value},
        )
