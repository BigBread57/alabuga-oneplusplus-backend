from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.constants import GenerateObjectType
from game_world.models import GameWorld


class GameWorldListSerializer(serializers.ModelSerializer):
    """
    Игровой мир. Список.
    """

    class Meta:
        model = GameWorld
        fields = (
            "id",
            "name",
            "description",
            "color",
            "standard_experience",
            "standard_currency",
            "currency_name",
        )


class GameWorldDetailSerializer(serializers.ModelSerializer):
    """
    Игровой мир. Детальная информация.
    """

    class Meta:
        model = GameWorld
        fields = (
            "id",
            "name",
            "description",
            "color",
            "standard_experience",
            "standard_currency",
            "currency_name",
        )


class GameWorldCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Игровой мир. Создание.
    """

    class Meta:
        model = GameWorld
        fields = (
            "name",
            "description",
            "color",
            "standard_experience",
            "standard_currency",
            "currency_name",
        )


class GameWorldGlobalStatisticsSerializer(serializers.Serializer):
    """
    Игровой мир. Рейтинг.
    """

    character_ranks = serializers.DictField(
        label=_("Информация по рангам персонажей"),
        help_text=_("Информация по рангам персонажей"),
    )
    character_competencies = serializers.DictField(
        label=_("Информация по компетенциям персонажей"),
        help_text=_("Информация по компетенциям персонажей"),
    )


class GameWorldStatisticsSerializer(serializers.Serializer):
    """
    Игровой мир. Статистика.
    """

    grouping_character_by_ranks = serializers.ListSerializer(
        child=serializers.DictField(),
        label=_("Группировка персонажей по рангам"),
        help_text=_("Группировка персонажей по рангам"),
    )
    number_of_character_who_closed_the_mission_branch = serializers.ListSerializer(
        child=serializers.DictField(),
        label=_("Количество персонажей, закрывших ветки миссий"),
        help_text=_("Количество персонажей, закрывших ветки миссий"),
    )
    number_of_character_who_closed_the_mission = serializers.ListSerializer(
        child=serializers.DictField(),
        label=_("Количество персонажей, закрывших миссии"),
        help_text=_("Количество персонажей, закрывших миссии"),
    )
    completed_or_failed_character_missions = serializers.ListSerializer(
        child=serializers.DictField(),
        label=_("Выполненные и проваленные миссии по дням"),
        help_text=_("Выполненные и проваленные миссии по дням"),
    )


class GameWorldGenerateSerializer(serializers.Serializer):
    """
    Игровой мир. Генерация.
    """

    rank_generate_type = serializers.ChoiceField(
        label=_("Тип генерации рангов"),
        help_text=_("Тип генерации рангов"),
        choices=GenerateObjectType.choices,
    )
    competency_generate_type = serializers.ChoiceField(
        label=_("Тип генерации компетенций"),
        help_text=_("Тип генерации компетенций"),
        choices=GenerateObjectType.choices,
    )
    required_rank_competency_generate_type = serializers.ChoiceField(
        label=_("Тип генерации требований к компетенциям"),
        help_text=_("Тип генерации требований к компетенциям"),
        choices=GenerateObjectType.choices,
    )
    activity_category_competency_generate_type = serializers.ChoiceField(
        label=_("Тип генерации категорий активности"),
        help_text=_("Тип генерации категорий активности"),
        choices=GenerateObjectType.choices,
    )
    artifact_generate_type = serializers.ChoiceField(
        label=_("Тип генерации артефакта"),
        help_text=_("Тип генерации артефакта"),
        choices=GenerateObjectType.choices,
    )
    event_generate_type = serializers.ChoiceField(
        label=_("Тип генерации событий"),
        help_text=_("Тип генерации событий"),
        choices=GenerateObjectType.choices,
    )
    event_artifact_generate_type = serializers.ChoiceField(
        label=_("Тип генерации артефактов событий"),
        help_text=_("Тип генерации артефактов событий"),
        choices=GenerateObjectType.choices,
    )
    event_competency_generate_type = serializers.ChoiceField(
        label=_("Тип генерации компетенций событий"),
        help_text=_("Тип генерации компетенций событий"),
        choices=GenerateObjectType.choices,
    )
    game_world_story_generate_type = serializers.ChoiceField(
        label=_("Тип генерации историй игрового мира"),
        help_text=_("Тип генерации историй игрового мира"),
        choices=GenerateObjectType.choices,
    )
    mission_generate_type = serializers.ChoiceField(
        label=_("Тип генерации миссий"),
        help_text=_("Тип генерации миссий"),
        choices=GenerateObjectType.choices,
    )
    mission_artifact_generate_type = serializers.ChoiceField(
        label=_("Тип генерации артефактов миссий"),
        help_text=_("Тип генерации артефактов миссий"),
        choices=GenerateObjectType.choices,
    )
    mission_competency_generate_type = serializers.ChoiceField(
        label=_("Тип генерации компетенций миссий"),
        help_text=_("Тип генерации компетенций миссий"),
        choices=GenerateObjectType.choices,
    )
    mission_branch_generate_type = serializers.ChoiceField(
        label=_("Тип генерации веток миссий"),
        help_text=_("Тип генерации веток миссий"),
        choices=GenerateObjectType.choices,
    )
    mission_level_generate_type = serializers.ChoiceField(
        label=_("Тип генерации уровней сложности миссий"),
        help_text=_("Тип генерации уровней сложности миссий"),
        choices=GenerateObjectType.choices,
    )


class GameWorldInfoForGenerateSerializer(serializers.Serializer):
    """
    Игровой мир. Информация для генерации
    """

    field_name = serializers.CharField(
        label=_("Название поля"),
        help_text=_("Название поля"),
    )
    description = serializers.CharField(
        label=_("Описание"),
        help_text=_("Описание"),
    )


class GameWorldDataAfterGenerateSerializer(serializers.Serializer):
    """
    Игровой мир. Информация для генерации.
    """

    competencies = serializers.ListSerializer(
        label=_("Список компетенций"),
        help_text=_("Список компетенций"),
        child=serializers.DictField(),
        allow_null=True,
    )
    ranks = serializers.ListSerializer(
        label=_("Список рангов"),
        help_text=_("Список рангов"),
        child=serializers.DictField(),
        allow_null=True,
    )
    required_rank_competencies = serializers.ListSerializer(
        label=_("Требования к компетенциям для рангов"),
        help_text=_("Требования к компетенциям для рангов"),
        child=serializers.DictField(),
        allow_null=True,
    )
    activity_categories = serializers.ListSerializer(
        label=_("Категории активностей"),
        help_text=_("Категории активностей"),
        child=serializers.DictField(),
        allow_null=True,
    )
    artifacts = serializers.ListSerializer(
        label=_("Список артефактов"),
        help_text=_("Список артефактов"),
        child=serializers.DictField(),
        allow_null=True,
    )
    events = serializers.ListSerializer(
        label=_("Список событий"),
        help_text=_("Список событий"),
        child=serializers.DictField(),
        allow_null=True,
    )
    event_artifacts = serializers.ListSerializer(
        label=_("Артефакты за события"),
        help_text=_("Артефакты за события"),
        child=serializers.DictField(),
        allow_null=True,
    )
    event_competencies = serializers.ListSerializer(
        label=_("Компетенции за события"),
        help_text=_("Компетенции за события"),
        child=serializers.DictField(),
        allow_null=True,
    )
    game_world_stories = serializers.ListSerializer(
        label=_("Истории игрового мира"),
        help_text=_("Истории игрового мира"),
        child=serializers.DictField(),
        allow_null=True,
    )
    missions = serializers.ListSerializer(
        label=_("Список миссий"),
        help_text=_("Список миссий"),
        child=serializers.DictField(),
        allow_null=True,
    )
    mission_artifacts = serializers.ListSerializer(
        label=_("Артефакты за миссии"),
        help_text=_("Артефакты за миссии"),
        child=serializers.DictField(),
        allow_null=True,
    )
    mission_branches = serializers.ListSerializer(
        label=_("Ветки миссий"),
        help_text=_("Ветки миссий"),
        child=serializers.DictField(),
        allow_null=True,
    )
    mission_competencies = serializers.ListSerializer(
        label=_("Компетенции за миссии"),
        help_text=_("Компетенции за миссии"),
        child=serializers.DictField(),
        allow_null=True,
    )
    mission_levels = serializers.ListSerializer(
        label=_("Уровни сложности миссий"),
        help_text=_("Уровни сложности миссий"),
        child=serializers.DictField(),
        allow_null=True,
    )


class GameWorldUpdateOrCreateAllEntitiesSerializer(serializers.Serializer):
    """
    Игровой мир. Информация или создание всех объектов.
    """

    competencies = serializers.ListSerializer(
        label=_("Список компетенций"),
        help_text=_("Список компетенций"),
        child=serializers.DictField(),
        allow_null=True,
    )
    ranks = serializers.ListSerializer(
        label=_("Список рангов"),
        help_text=_("Список рангов"),
        child=serializers.DictField(),
        allow_null=True,
    )
    required_rank_competencies = serializers.ListSerializer(
        label=_("Требования к компетенциям для рангов"),
        help_text=_("Требования к компетенциям для рангов"),
        child=serializers.DictField(),
        allow_null=True,
    )
    activity_categories = serializers.ListSerializer(
        label=_("Категории активностей"),
        help_text=_("Категории активностей"),
        child=serializers.DictField(),
        allow_null=True,
    )
    artifacts = serializers.ListSerializer(
        label=_("Список артефактов"),
        help_text=_("Список артефактов"),
        child=serializers.DictField(),
        allow_null=True,
    )
    events = serializers.ListSerializer(
        label=_("Список событий"),
        help_text=_("Список событий"),
        child=serializers.DictField(),
        allow_null=True,
    )
    event_artifacts = serializers.ListSerializer(
        label=_("Артефакты за события"),
        help_text=_("Артефакты за события"),
        child=serializers.DictField(),
        allow_null=True,
    )
    event_competencies = serializers.ListSerializer(
        label=_("Компетенции за события"),
        help_text=_("Компетенции за события"),
        child=serializers.DictField(),
        allow_null=True,
    )
    game_world_stories = serializers.ListSerializer(
        label=_("Истории игрового мира"),
        help_text=_("Истории игрового мира"),
        child=serializers.DictField(),
        allow_null=True,
    )
    missions = serializers.ListSerializer(
        label=_("Список миссий"),
        help_text=_("Список миссий"),
        child=serializers.DictField(),
        allow_null=True,
    )
    mission_artifacts = serializers.ListSerializer(
        label=_("Артефакты за миссии"),
        help_text=_("Артефакты за миссии"),
        child=serializers.DictField(),
        allow_null=True,
    )
    mission_branches = serializers.ListSerializer(
        label=_("Ветки миссий"),
        help_text=_("Ветки миссий"),
        child=serializers.DictField(),
        allow_null=True,
    )
    mission_competencies = serializers.ListSerializer(
        label=_("Компетенции за миссии"),
        help_text=_("Компетенции за миссии"),
        child=serializers.DictField(),
        allow_null=True,
    )
    mission_levels = serializers.ListSerializer(
        label=_("Уровни сложности миссий"),
        help_text=_("Уровни сложности миссий"),
        child=serializers.DictField(),
        allow_null=True,
    )


class GameWorldGlobalStatisticsSerializer(serializers.Serializer):
    """
    Игровой мир. Глобальная статистика.
    """

    missions = serializers.DictField(
        label=_("Статистика по миссиям"),
        help_text=_("Статистика по миссиям"),
    )
    events = serializers.DictField(
        label=_("Статистика по событиям"),
        help_text=_("Статистика по событиям"),
    )
    artifacts = serializers.DictField(
        label=_("Статистика по артефактам"),
        help_text=_("Статистика по артефактам"),
    )
    competencies = serializers.DictField(
        label=_("Статистика по компетенциям"),
        help_text=_("Статистика по компетенциям"),
    )
