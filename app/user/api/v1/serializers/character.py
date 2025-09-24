from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.api.v1.serializers.nested import RankNestedSerializer
from game_world.api.v1.serializers.nested import GameWorldNestedSerializer
from user.api.v1.serializers.nested import (
    CharacterArtifactNestedSerializer,
    CharacterCompetencyNestedSerializer,
    CharacterEventNestedSerializer,
    CharacterMissionNestedSerializer,
    UserNestedSerializer,
)
from user.models import Character


class CharacterActualForUserSerializer(serializers.ModelSerializer):
    """
    Персонаж пользователя. Детальная информация.
    """

    user = UserNestedSerializer(
        label=_("Пользователь"),
        help_text=_("Пользователь"),
    )
    game_world = GameWorldNestedSerializer(
        label=_("Игровой мир"),
        help_text=_("Игровой мир"),
    )
    rank = RankNestedSerializer(
        label=_("Ранг"),
        help_text=_("Ранг"),
    )
    character_artifacts = CharacterArtifactNestedSerializer(
        label=_("Артефакты"),
        help_text=_("Артефакты"),
        many=True,
    )
    character_competencies = CharacterCompetencyNestedSerializer(
        label=_("Компетенции"),
        help_text=_("Компетенции"),
        many=True,
    )
    character_missions = CharacterMissionNestedSerializer(
        label=_("Миссии"),
        help_text=_("Миссии"),
        many=True,
    )
    character_events = CharacterEventNestedSerializer(
        label=_("События"),
        help_text=_("События"),
        many=True,
    )

    class Meta:
        model = Character
        fields = (
            "id",
            "avatar",
            "experience",
            "currency",
            "is_active",
            "user",
            "game_world",
            "rank",
            "character_artifacts",
            "character_competencies",
            "character_missions",
            "character_events",
        )
