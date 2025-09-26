from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.api.v1.serializers.nested import GameWorldNestedSerializer
from user.api.v1.serializers.nested import (
    CharacterRankNestedSerializer,
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
    character_rank = serializers.SerializerMethodField(
        label=_("Ранг"),
        help_text=_("Ранг"),
    )

    class Meta:
        model = Character
        fields = (
            "id",
            "avatar",
            "currency",
            "is_active",
            "user",
            "game_world",
            "character_rank",
        )

    def get_character_rank(self, character: Character) -> dict[str, Any] | None:
        """
        Ранг пользователя.
        """
        return CharacterRankNestedSerializer(
            instance=character.character_ranks.select_related("rank").filter(is_received=False).first(),
            context=self.context,
        ).data


class CharacterUpdateSerializer(serializers.ModelSerializer):
    """
    Персонаж. Изменение.
    """

    class Meta:
        model = Character
        fields = ("avatar",)
