from django.contrib import admin

from game_mechanics.models import (
    Competency,
    Rank,
    RequiredRankCompetency,
)


class RequiredRankCompetencyInline(admin.TabularInline):
    """
    Требования к компетенциям для получения ранга.
    """

    model = RequiredRankCompetency
    extra = 1


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    """
    Ранг.
    """

    list_display = (
        "id",
        "name",
        "parent",
        "required_experience",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = ("-id",)
    inlines = [RequiredRankCompetencyInline]


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    """
    Компетенция.
    """

    list_display = (
        "id",
        "name",
        "required_experience",
        "game_world",
    )
    search_fields = (
        "name",
        "description",
    )
    list_filter = (
        "game_world",
    )
    autocomplete_fields = (
        "game_world",
    )
    list_select_related = (
        "game_world",
    )
    ordering = ("-id",)


@admin.register(RequiredRankCompetency)
class RequiredRankCompetencyAdmin(admin.ModelAdmin):
    """
    Требования к компетенциям для получения ранга.
    """

    list_display = (
        "id",
        "rank",
        "competency",
        "required_experience",
    )
    ordering = ("-id",)
    autocomplete_fields = (
        "rank",
        "competency",
    )
    list_select_related = (
        "rank",
        "competency",
    )
