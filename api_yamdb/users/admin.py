from django.contrib import admin

from api_yamdb.settings import USERS_PER_PAGE
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
    )
    list_editable = ("role",)
    list_filter = ("username",)
    list_per_page = USERS_PER_PAGE
    search_fields = ("username", "role")
    empty_value_display = "-пусто-"
