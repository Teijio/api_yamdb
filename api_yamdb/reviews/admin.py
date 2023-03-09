from django.conf import settings
from django.contrib import admin

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки раздела категорий."""

    list_display = ("id", "name", "slug")
    empty_value_display = "-пусто-"
    list_filter = ("name",)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка раздела комментариев."""

    list_display = ("id", "author", "text", "pub_date", "review")
    empty_value_display = "-пусто-"
    list_filter = ("author", "pub_date")
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ("author",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка раздела жанров."""

    list_display = ("id", "name", "slug")
    empty_value_display = "-пусто-"
    list_filter = ("name",)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройка раздела отзывов."""

    list_display = ("id", "author", "text", "score", "pub_date", "title")
    empty_value_display = "-пусто-"
    list_filter = ("author", "score", "pub_date")
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ("author",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка раздела произведений."""

    list_display = (
        "id",
        "name",
        "year",
        "description",
        "category",
    )
    empty_value_display = "-пусто-"
    list_filter = ("name",)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ("name", "year", "category")
