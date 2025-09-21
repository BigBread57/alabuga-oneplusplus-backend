from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Artifact,
    BoardingStep,
    Competency,
    Rank,
    RankCompetencyRequirement,
    UserArtifact,
    UserBoardingProgress,
    UserCompetency,
    UserRank,
)


class RankCompetencyRequirementInline(admin.TabularInline):
    """Инлайн для требований к компетенциям."""

    model = RankCompetencyRequirement
    extra = 1


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    """Административная панель для рангов."""

    list_display = ("name", "order", "experience_required", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "description")
    ordering = ("order",)
    inlines = [RankCompetencyRequirementInline]


@admin.register(Competency)
class CompetencyAdmin(admin.ModelAdmin):
    """Административная панель для компетенций."""

    list_display = ("name", "created_at")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    """Административная панель для артефактов."""

    list_display = ("name", "rarity", "created_at")
    list_filter = ("rarity", "created_at")
    search_fields = ("name", "description")
    ordering = ("-created_at",)


@admin.register(UserRank)
class UserRankAdmin(admin.ModelAdmin):
    """Административная панель для рангов пользователей."""

    list_display = ("user", "rank", "created_at")
    list_filter = ("rank", "created_at")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    ordering = ("-created_at",)


@admin.register(UserCompetency)
class UserCompetencyAdmin(admin.ModelAdmin):
    """Административная панель для компетенций пользователей."""

    list_display = ("user", "competency", "level", "updated_at")
    list_filter = ("competency", "level", "updated_at")
    search_fields = ("user__username", "competency__name")
    ordering = ("-updated_at",)


@admin.register(UserArtifact)
class UserArtifactAdmin(admin.ModelAdmin):
    """Административная панель для артефактов пользователей."""

    list_display = ("user", "artifact", "created_at")
    list_filter = ("artifact__rarity", "created_at")
    search_fields = ("user__username", "artifact__name")
    ordering = ("-created_at",)


@admin.register(BoardingStep)
class BoardingStepAdmin(admin.ModelAdmin):
    """Административная панель для шагов онбординга."""

    list_display = ("title", "order", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "content")
    ordering = ("order",)


@admin.register(UserBoardingProgress)
class UserBoardingProgressAdmin(admin.ModelAdmin):
    """Административная панель для прогресса онбординга."""

    list_display = ("user", "step", "completed_at", "created_at")
    list_filter = ("completed_at", "step", "created_at")
    search_fields = ("user__username", "step__title")
    ordering = ("-created_at",)
