from django.db import models


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Category(models.Model):
    name = models.CharField(unique=True, max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField(unique=True, max_length=256)
    year = models.IntegerField(unique=True)
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='reviews',
        unique=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='reviews',
        unique=True
    )
