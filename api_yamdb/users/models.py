from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ("user", "Пользователь"),
    ("moderator", "Модератор"),
    ("admin", "Администратор"),
)


class User(AbstractUser):
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(default="user", max_length=30, choices=CHOICES)
    email = models.EmailField(max_length=254, unique=True, blank=False)
