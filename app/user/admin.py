from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from app.user.models.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Пользователь.
    """

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Персональная информация"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "role",
                    "phone",
                    "email",
                ),
            },
        ),
        (
            _("Права доступа"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "middle_name", "role", "phone", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "first_name", "last_name", "middle_name", "phone", "email")
    ordering = ("-id",)
