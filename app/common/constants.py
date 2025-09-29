from django.db import models
from django.utils.translation import gettext_lazy as _


class CharacterRoles(models.TextChoices):
    """
    Роли пользователей.
    """

    CANDIDATE = "CANDIDATE", _("Кандидат")
    EMPLOYEE = "EMPLOYEE", _("Сотрудник")
    MANAGER = "MANAGER", _("Менеджер")
    CONTENT_MANAGER = "CONTENT_MANAGER", _("Контент-менеджер")
    HR = "HR", _("HR")
    ORGANIZER = "ORGANIZER", _("Организатор")
    ADMIN = "ADMIN", _("Администратор")


class GenerateObjectType(models.TextChoices):
    """
    Тип генерации объектов.
    """

    NEW = "NEW", _("Создать новые объекты")
    ADVICE = "ADVICE", _(
        "Проанализировать существующие объекты, улучшить или оптимизировать их и при необходимости добавить новые."
        "При улучшении или оптимизации старого объекта поле uuid менять запрещено."
    )


class FieldNameForGenerate:
    """
    Названия полей для генерации.
    """

    RANK_GENERATE_TYPE = "rank_generate_type"
    COMPETENCY_GENERATE_TYPE = "competency_generate_type"
    REQUIRED_RANK_COMPETENCY_GENERATE_TYPE = "required_rank_competency_generate_type"
    ACTIVITY_CATEGORY_GENERATE_TYPE = "activity_category_generate_type"
    ARTIFACT_GENERATE_TYPE = "artifact_generate_type"
    EVENT_GENERATE_TYPE = "event_generate_type"
    EVENT_ARTIFACT_GENERATE_TYPE = "event_artifact_generate_type"
    EVENT_COMPETENCY_GENERATE_TYPE = "event_competency_generate_type"
    GAME_WORLD_STORY_GENERATE_TYPE = "game_world_story_generate_type"
    MISSION_GENERATE_TYPE = "mission_generate_type"
    MISSION_ARTIFACT_GENERATE_TYPE = "mission_artifact_generate_type"
    MISSION_COMPETENCY_GENERATE_TYPE = "mission_competency_generate_type"
    MISSION_BRANCH_GENERATE_TYPE = "mission_branch_generate_type"
    MISSION_LEVEL_GENERATE_TYPE = "mission_level_generate_type"

    ALL = {
        RANK_GENERATE_TYPE,
        COMPETENCY_GENERATE_TYPE,
        REQUIRED_RANK_COMPETENCY_GENERATE_TYPE,
        ACTIVITY_CATEGORY_GENERATE_TYPE,
        ARTIFACT_GENERATE_TYPE,
        EVENT_GENERATE_TYPE,
        EVENT_ARTIFACT_GENERATE_TYPE,
        EVENT_COMPETENCY_GENERATE_TYPE,
        GAME_WORLD_STORY_GENERATE_TYPE,
        MISSION_GENERATE_TYPE,
        MISSION_ARTIFACT_GENERATE_TYPE,
        MISSION_COMPETENCY_GENERATE_TYPE,
        MISSION_BRANCH_GENERATE_TYPE,
        MISSION_LEVEL_GENERATE_TYPE,
    }
