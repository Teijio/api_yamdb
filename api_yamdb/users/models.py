from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Класс пользователей."""

    ROLES = (
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Электронный почтовый ящик",
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Описание пользователя",
    )
    role = models.CharField(
        default=settings.USER,
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
        ordering = ("username",)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR

    @property
    def is_admin(self):
        return self.role == settings.ADMIN or self.is_superuser
