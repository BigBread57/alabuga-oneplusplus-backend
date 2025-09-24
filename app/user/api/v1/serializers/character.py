from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.api.v1.serializers.nested import RankNestedSerializer
from game_world.api.v1.serializers.nested import GameWorldNestedSerializer
from user.api.v1.serializers.nested import (
    CharacterArtifactNestedSerializer,
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
    rank = serializers.SerializerMethodField(
        label=_("Ранг"),
        help_text=_("Ранг"),
    )
    character_artifacts = CharacterArtifactNestedSerializer(
        label=_("Артефакты пользователя"),
        help_text=_("Артефакты пользователя"),
        many=True,
    )
    character_competencies = serializers.SerializerMethodField(
        label=_("Компетенции пользователя"),
        help_text=_("Компетенции пользователя"),
    )
    character_missions = CharacterMissionNestedSerializer(
        label=_("Миссии пользователя"),
        help_text=_("Миссии пользователя"),
        many=True,
    )
    character_events = CharacterEventNestedSerializer(
        label=_("События пользователя"),
        help_text=_("События пользователя"),
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

    def get_rank(self, character: Character) -> dict[str, Any]:
        """
        Ранг пользователя.
        """
        return RankNestedSerializer(
            instance=character.character_ranks.filter(is_received=False).first(),
        ).data

    def get_character_competencies(self, character: Character) -> dict[str, Any]:
        """
        Ранг пользователя.
        """
        return RankNestedSerializer(
            instance=character.character_competencies.filter(is_received=False),
            many=True,
        ).data
