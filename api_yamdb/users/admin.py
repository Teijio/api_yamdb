from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


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
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ("username", "role")
    empty_value_display = "-пусто-"
