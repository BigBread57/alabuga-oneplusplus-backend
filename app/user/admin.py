from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from app.user.models.profile import Profile


@admin.register(Profile)
class ProfileAdmin(BaseUserAdmin):
    """Административная панель для пользователей."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'experience', 'mana', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Геймификация'), {
            'fields': ('role', 'experience', 'mana', 'avatar'),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Дополнительная информация'), {
            'fields': ('first_name', 'last_name', 'email', 'role'),
        }),
    )
