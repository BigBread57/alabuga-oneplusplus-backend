from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Mission,
    MissionArtifact,
    MissionBranch,
    MissionCompetency,
    RankMission,
    UserMission,
)


class MissionCompetencyInline(admin.TabularInline):
    """Инлайн для компетенций миссии."""

    model = MissionCompetency
    extra = 1


class MissionArtifactInline(admin.TabularInline):
    """Инлайн для артефактов миссии."""

    model = MissionArtifact
    extra = 1


@admin.register(MissionBranch)
class MissionBranchAdmin(admin.ModelAdmin):
    """Административная панель для веток миссий."""

    list_display = ("name", "category", "order", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    ordering = ("category", "order")


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    """Административная панель для миссий."""

    list_display = ("name", "branch", "experience_reward", "mana_reward", "is_key_mission", "is_active")
    list_filter = ("branch", "is_key_mission", "is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("branch", "order")
    filter_horizontal = ("required_missions",)
    inlines = [MissionCompetencyInline, MissionArtifactInline]

    fieldsets = (
        (
            _("Основная информация"),
            {
                "fields": ("name", "description", "branch", "order"),
            },
        ),
        (
            _("Награды"),
            {
                "fields": ("experience_reward", "mana_reward"),
            },
        ),
        (
            _("Условия доступа"),
            {
                "fields": ("min_rank", "required_missions"),
            },
        ),
        (
            _("Настройки"),
            {
                "fields": ("is_key_mission", "is_active"),
            },
        ),
    )


@admin.register(UserMission)
class UserMissionAdmin(admin.ModelAdmin):
    """Административная панель для миссий пользователей."""

    list_display = ("user", "mission", "status", "started_at", "completed_at", "reviewed_by")
    list_filter = ("status", "mission__branch", "started_at", "completed_at")
    search_fields = ("user__username", "mission__name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            _("Основная информация"),
            {
                "fields": ("user", "mission", "status"),
            },
        ),
        (
            _("Временные отметки"),
            {
                "fields": ("started_at", "completed_at", "created_at", "updated_at"),
            },
        ),
        (
            _("Результат и проверка"),
            {
                "fields": ("result", "reviewed_by", "review_comment"),
            },
        ),
    )


@admin.register(RankMission)
class RankMissionAdmin(admin.ModelAdmin):
    """Административная панель для обязательных миссий рангов."""

    list_display = ("rank", "mission", "created_at")
    list_filter = ("rank", "mission__branch", "created_at")
    search_fields = ("rank__name", "mission__name")
    ordering = ("rank__order", "mission__order")
