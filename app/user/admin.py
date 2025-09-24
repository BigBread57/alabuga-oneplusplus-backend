from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from user.models import Character, CharacterArtifact, CharacterCompetency, CharacterEvent, CharacterMission
from user.models.character_rank import CharacterRank
from user.models.user import User


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
        (
            _("Важные даты"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "role",
        "phone",
        "is_staff",
    )
    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "middle_name",
        "phone",
        "email",
    )
    ordering = ("-id",)


class CharacterArtifactInline(admin.TabularInline):
    """
    Артефакты персонажа.
    """

    model = CharacterArtifact
    extra = 1


class CharacterCompetencyInline(admin.TabularInline):
    """
    Уровень компетенции персонажа.
    """

    model = CharacterCompetency
    extra = 1


class CharacterEventInline(admin.TabularInline):
    """
    Прогресс персонажа по событиям.
    """

    model = CharacterEvent
    extra = 1


class CharacterMissionInline(admin.TabularInline):
    """
    Прогресс персонажа по миссиям.
    """

    model = CharacterMission
    extra = 1


class CharacterRankInline(admin.TabularInline):
    """
    Прогресс персонажа по рангам.
    """

    model = CharacterRank
    extra = 1


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """
    Персонаж пользователя.
    """

    list_display = (
        "id",
        "currency",
        "is_active",
        "user",
        "game_world",
    )
    list_filter = ("is_active",)
    autocomplete_fields = (
        "user",
        "game_world",
    )
    list_select_related = (
        "user",
        "game_world",
    )
    ordering = ("-id",)
    inlines = (
        CharacterArtifactInline,
        CharacterCompetencyInline,
        CharacterEventInline,
        CharacterMissionInline,
        CharacterRankInline,
    )


#
# @admin.register(CharacterArtifact)
# class CharacterArtifactAdmin(admin.ModelAdmin):
#     """
#     Артефакты персонажа.
#     """
#
#     list_display = (
#         "id",
#         "character",
#         "artifact",
#     )
#     list_filter = (
#         "artifact__name",
#     )
#     autocomplete_fields = (
#         "character",
#         "artifact",
#     )
#     list_select_related = (
#         "character",
#         "artifact",
#     )
#     ordering = ("-id",)
#
#
# @admin.register(CharacterCompetency)
# class CharacterCompetencyAdmin(admin.ModelAdmin):
#     """
#     Уровень компетенции персонажа.
#     """
#
#     list_display = (
#         "id",
#         "character",
#         "competency",
#         "level",
#     )
#     list_filter = (
#         "competency__name",
#     )
#     autocomplete_fields = (
#         "character",
#         "competency",
#     )
#     list_select_related = (
#         "character",
#         "competency",
#     )
#     ordering = ("-id",)
#
#
# @admin.register(CharacterEvent)
# class CharacterEventAdmin(admin.ModelAdmin):
#     """
#     Прогресс персонажа по событиям.
#     """
#
#     list_display = (
#         "id",
#         "status",
#         "start_datetime",
#         "end_datetime",
#         "character",
#         "event",
#         "inspector",
#     )
#     list_filter = (
#         "status",
#     )
#     autocomplete_fields = (
#         "character",
#         "event",
#         "inspector",
#     )
#     list_select_related = (
#         "character",
#         "event",
#         "inspector",
#     )
#     ordering = ("-id",)
#
#
# @admin.register(CharacterMission)
# class CharacterMissionAdmin(admin.ModelAdmin):
#     """
#     Прогресс персонажа по миссиям.
#     """
#
#     list_display = (
#         "id",
#         "status",
#         "start_datetime",
#         "end_datetime",
#         "character",
#         "mission",
#         "inspector",
#     )
#     list_filter = (
#         "status",
#     )
#     autocomplete_fields = (
#         "character",
#         "mission",
#         "inspector",
#     )
#     list_select_related = (
#         "character",
#         "mission",
#         "inspector",
#     )
#     ordering = ("-id",)
