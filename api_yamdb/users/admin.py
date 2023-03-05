from django.contrib import admin

from api_yamdb.settings import LIST_PER_PAGE
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка для пользователей."""

    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
    )
    list_editable = ("role",)
    list_filter = ("username",)
    list_per_page = LIST_PER_PAGE
    search_fields = ("username", "role")
    empty_value_display = "-пусто-"
