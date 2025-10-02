from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.models import Competency, Rank
from game_world.models import (
    ActivityCategory,
    Artifact,
    Event,
    GameWorld,
    Mission,
    MissionBranch,
    MissionLevel,
    GameWorldStory,
)
from user.api.v1.serializers.nested import CharacterNestedSerializer


class GameWorldStoryAllInfoNestedSerializer(serializers.ModelSerializer):
    """
    Игровая история мира. Вложенный сериалайзер.
    """

    class Meta:
        model = GameWorldStory
        fields = (
            "id",
            "uuid",
            "image",
            "text",
        )


class CompetencyAllInfoNestedSerializer(serializers.ModelSerializer):
    """
    Компетенция. Полная информация. Вложенный сериалайзер.
    """

    game_world_stories = GameWorldStoryAllInfoNestedSerializer(
        label=_("История игрового мира"),
        help_text=_("История игрового мира"),
        many=True,
    )
    parent = serializers.SerializerMethodField(
        label=_("Родительская компетенция"),
        help_text=_("Родительская компетенция"),
    )

    class Meta:
        model = Competency
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "level",
            "required_experience",
            "icon",
            "color",
            "parent",
            "game_world_stories",
        )

    def get_parent(self, competency: Competency) -> "CompetencyAllInfoNestedSerializer":
        """Рекурсивно получаем всю цепочку родителей"""
        if competency.parent:
            return CompetencyAllInfoNestedSerializer(instance=competency.parent, context=self.context).data
        return None


class ArtifactAllInfoNestedSerializer(serializers.ModelSerializer):
    """
    Артефакт. Полная информация. Вложенный сериалайзер.
    """

    game_world_stories = GameWorldStoryAllInfoNestedSerializer(
        label=_("История игрового мира"),
        help_text=_("История игрового мира"),
        many=True,
    )

    class Meta:
        model = Artifact
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "icon",
            "color",
            "modifier",
            "modifier_value",
            "game_world_stories",
        )


class MissionLevelAllNestedNestedSerializer(serializers.ModelSerializer):
    """
    Категория активности. Вложенный сериалайзер.
    """

    class Meta:
        model = MissionLevel
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "icon",
            "color",
            "multiplier_experience",
            "multiplier_currency",
        )


class ActivityCategoryAllNestedNestedSerializer(serializers.ModelSerializer):
    """
    Категория активности. Вложенный сериалайзер.
    """

    class Meta:
        model = ActivityCategory
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "icon",
            "color",
        )


class MissionAllInfoNestedSerializer(serializers.ModelSerializer):
    """
    Миссия. Вложенный сериалайзер.
    """

    artifacts = ArtifactAllInfoNestedSerializer(
        label=_("Артефакт"),
        help_text=_("Артефакт"),
        many=True,
    )
    competencies = CompetencyAllInfoNestedSerializer(
        label=_("Компетенции"),
        help_text=_("Компетенции"),
        many=True,
    )
    game_world_stories = GameWorldStoryAllInfoNestedSerializer(
        label=_("История игрового мира"),
        help_text=_("История игрового мира"),
        many=True,
    )
    level = MissionLevelAllNestedNestedSerializer(
        label=_("Уровень"),
        help_text=_("Уровень"),
    )
    category = ActivityCategoryAllNestedNestedSerializer(
        label=_("Категория активности"),
        help_text=_("Категория активности"),
    )
    mentor = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
    )

    class Meta:
        model = Mission
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "experience",
            "currency",
            "icon",
            "color",
            "order",
            "is_key_mission",
            "is_active",
            "time_to_complete",
            "level",
            "category",
            "mentor",
            "artifacts",
            "competencies",
            "game_world_stories",
        )


class MissionBranchAllInfoNestedSerializer(serializers.ModelSerializer):
    """
    Ветка миссий. Полная информация. Вложенный сериалайзер.
    """

    category = ActivityCategoryAllNestedNestedSerializer(
        label=_("Категория активности"),
        help_text=_("Категория активности"),
    )
    missions = MissionAllInfoNestedSerializer(
        label=_("Миссии"),
        help_text=_("Миссии"),
        many=True,
    )
    mentor = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
    )

    class Meta:
        model = MissionBranch
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "icon",
            "color",
            "is_active",
            "start_datetime",
            "time_to_complete",
            "mentor",
            "category",
            "missions",
        )


class EventAllInfoNestedSerializer(serializers.ModelSerializer):
    """
    Событие. Вложенный сериалайзер.
    """

    category = ActivityCategoryAllNestedNestedSerializer(
        label=_("Категория активности"),
        help_text=_("Категория активности"),
    )
    artifacts = ArtifactAllInfoNestedSerializer(
        label=_("Артефакт"),
        help_text=_("Артефакт"),
        many=True,
    )
    competencies = CompetencyAllInfoNestedSerializer(
        label=_("Компетенции"),
        help_text=_("Компетенции"),
        many=True,
    )
    game_world_stories = GameWorldStoryAllInfoNestedSerializer(
        label=_("История игрового мира"),
        help_text=_("История игрового мира"),
        many=True,
    )
    mentor = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "experience",
            "currency",
            "icon",
            "color",
            "required_number",
            "is_active",
            "start_datetime",
            "time_to_complete",
            "category",
            "mentor",
            "artifacts",
            "competencies",
            "game_world_stories",
        )


class RankParentNestedSerializer(serializers.ModelSerializer):
    """
    Ранг. Вложенный сериалайзер.
    """

    class Meta:
        model = Rank
        fields = ("id", "uuid")


class RankAllInfoNestedSerializer(serializers.ModelSerializer):
    """
    Ранг. Полная информация. Вложенный сериалайзер.
    """

    game_world_stories = GameWorldStoryAllInfoNestedSerializer(
        label=_("История игрового мира"),
        help_text=_("История игрового мира"),
        many=True,
    )
    mission_branches = MissionBranchAllInfoNestedSerializer(
        label=_("Ветки миссий"),
        help_text=_("Ветки миссий"),
        many=True,
    )
    events = EventAllInfoNestedSerializer(
        label=_("События"),
        help_text=_("События"),
        many=True,
    )
    parent = RankParentNestedSerializer(
        label=_("Родительский ранг"),
        help_text=_("Родительский ранг"),
    )

    class Meta:
        model = Rank
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "required_experience",
            "icon",
            "color",
            "parent",
            "mission_branches",
            "events",
            "game_world_stories",
            "required_rank_competencies",
        )


class GameWorldDataForGraphSerializer(serializers.ModelSerializer):
    """
    Игровой мир. Список.
    """

    ranks = RankAllInfoNestedSerializer(
        label=_("Ранги"),
        help_text=_("Ранги"),
        many=True,
    )

    class Meta:
        model = GameWorld
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "color",
            "standard_experience",
            "standard_currency",
            "currency_name",
            "ranks",
        )


class GameWorldDataForGraphSerializer(serializers.ModelSerializer):
    """
    Игровой мир. Список.
    """

    ranks = RankAllInfoNestedSerializer(
        label=_("Ранги"),
        help_text=_("Ранги"),
        many=True,
    )

    class Meta:
        model = GameWorld
        fields = (
            "id",
            "uuid",
            "name",
            "description",
            "color",
            "standard_experience",
            "standard_currency",
            "currency_name",
            "ranks",
        )
