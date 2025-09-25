from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.api.v1.serializers.nested import GameWorldNestedSerializer
from user.api.v1.serializers.nested import (
    CharacterArtifactNestedSerializer,
    CharacterEventNestedSerializer,
    CharacterMissionNestedSerializer,
    UserNestedSerializer, CharacterCompetencyNestedSerializer, CharacterRankNestedSerializer,
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
    # character_artifacts = CharacterArtifactNestedSerializer(
    #     label=_("Артефакты пользователя"),
    #     help_text=_("Артефакты пользователя"),
    #     many=True,
    # )
    # character_competencies = serializers.SerializerMethodField(
    #     label=_("Компетенции пользователя"),
    #     help_text=_("Компетенции пользователя"),
    # )
    # character_missions = CharacterMissionNestedSerializer(
    #     label=_("Миссии пользователя"),
    #     help_text=_("Миссии пользователя"),
    #     many=True,
    # )
    # character_events = CharacterEventNestedSerializer(
    #     label=_("События пользователя"),
    #     help_text=_("События пользователя"),
    #     many=True,
    # )

    class Meta:
        model = Character
        fields = (
            "id",
            "avatar",
            "currency",
            "is_active",
            "user",
            "game_world",
            "rank",
        )

    def get_rank(self, character: Character) -> dict[str, Any] | None:
        """
        Ранг пользователя.
        """
        return CharacterRankNestedSerializer(
            instance=character.character_ranks.select_related("rank").filter(is_received=False).first(),
            context=self.context,
        ).data
