from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import LENGTH_USERNAME


class User(AbstractUser):
    ROLES = (
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    )
    user = "user"
    moderator = "moderator"
    admin = "admin"
    username = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        blank=False,
        verbose_name="Имя пользователя",
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+\z",
                message="Имя пользователя содержит недопустимый символ",
            ),
        ],
    )
    email = models.EmailField(
        max_length=254, unique=True, blank=False, verbose_name="email"
    )
    first_name = models.CharField(
        max_length=150, verbose_name="Имя", blank=True
    )
    last_name = models.CharField(
        max_length=150, verbose_name="Фамилия", blank=True
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    role = models.CharField(
        default=user,
        max_length=20,
        choices=ROLES,
        verbose_name="Тип учетной записи",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=("username", "email"), name="unique_user"
            )
        ]
        ordering = ("id",)

    def __str__(self):
        return self.username[:LENGTH_USERNAME]

    @property
    def is_user(self):
        return self.role == self.user

    @property
    def is_moderator(self):
        return self.role == self.moderator

    @property
    def is_admin(self):
        return self.role == self.admin
