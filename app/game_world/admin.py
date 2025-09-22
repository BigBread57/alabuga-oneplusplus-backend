from django.contrib import admin

from .models import (
    Artifact,
    Event,
    EventCompetency,
    GameWorld,
    Mission,
    MissionArtifact,
    MissionBranch,
    MissionCategory,
    MissionCompetency,
    MissionLevel,
)


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    """
    Артефакт.
    """

    list_display = (
        "id",
        "name",
        "modifier",
        "modifier_value",
        "game_world",
    )
    list_filter = ("modifier", "game_world")
    search_fields = (
        "name",
        "description",
    )
    ordering = ("-id",)
    autocomplete_fields = ("game_world",)
    list_select_related = ("game_world",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Событие.
    """

    list_display = (
        "id",
        "name",
        "is_active",
        "category",
        "game_world",
    )
    list_filter = ("is_active", "category", "game_world")
    search_fields = (
        "name",
        "description",
    )
    ordering = ("-id",)
    autocomplete_fields = (
        "game_world",
        "is_active",
        "category",
    )
    list_select_related = (
        "game_world",
        "is_active",
        "category",
    )


@admin.register(EventCompetency)
class EventCompetencyAdmin(admin.ModelAdmin):
    """
    Прокачка компетенций за событие.
    """

    list_display = (
        "id",
        "event",
        "competency",
        "experience",
    )
    list_filter = ("competency",)
    ordering = ("-id",)
    autocomplete_fields = (
        "event",
        "competency",
    )
    list_select_related = (
        "event",
        "competency",
    )


@admin.register(GameWorld)
class GameWorldAdmin(admin.ModelAdmin):
    """
    Игровой мир.
    """

    list_display = (
        "id",
        "name",
        "description",
        "color",
        "standard_experience",
        "currency_name",
    )
    ordering = ("-id",)


class MissionCompetencyInline(admin.TabularInline):
    """
    Инлайн для компетенций миссии.
    """

    model = MissionCompetency
    extra = 1


class MissionArtifactInline(admin.TabularInline):
    """
    Инлайн для артефактов миссии.
    """

    model = MissionArtifact
    extra = 1


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    """
    Миссия.
    """

    list_display = ("id", "name", "branch", "experience_reward", "mana_reward", "is_key_mission")
    list_filter = ("branch", "is_key_mission", "is_active")
    search_fields = ("name", "description")
    ordering = ("-id",)
    filter_horizontal = ("required_missions", "artifacts")
    inlines = [MissionCompetencyInline, MissionArtifactInline]


@admin.register(MissionBranch)
class MissionBranchAdmin(admin.ModelAdmin):
    """
    Ветка миссий.
    """

    list_display = (
        "id",
        "name",
        "category",
        "order",
    )
    list_filter = ("category",)
    search_fields = ("name", "description")
    ordering = ("-id",)


@admin.register(MissionCompetency)
class MissionCompetencyAdmin(admin.ModelAdmin):
    """
    Прокачка компетенций за миссию.
    """

    list_display = ("id", "mission", "competency", "experience")
    search_fields = ("name",)
    ordering = ("-id",)
    autocomplete_fields = (
        "mission",
        "competency",
    )
    list_select_related = (
        "mission",
        "competency",
    )


@admin.register(MissionCategory)
class MissionCategoryAdmin(admin.ModelAdmin):
    """
    Категория миссии.
    """

    list_display = (
        "id",
        "name",
        "color",
    )
    search_fields = ("name",)
    ordering = ("-id",)


@admin.register(MissionLevel)
class MissionLevelAdmin(admin.ModelAdmin):
    """
    Уровень миссии.
    """

    list_display = ("id", "name", "color", "multiplier_experience", "multiplier_currency")
    search_fields = ("name",)
    ordering = ("-id",)
