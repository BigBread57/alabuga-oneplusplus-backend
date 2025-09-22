from django.contrib import admin

from app.game_mechanics.models import (
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
        "experience_required",
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
    )
    search_fields = (
        "name",
        "description",
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
        "required_level",
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
