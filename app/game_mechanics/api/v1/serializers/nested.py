from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.models import Competency, Rank
from game_world.api.v1.serializers.nested import GameWorldStoryNestedSerializer


class RankNestedSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Вложенный сериалайзер.
    """

    game_world_stories = GameWorldStoryNestedSerializer(
        label=_("История игрового мира"),
        help_text=_("История игрового мира"),
        many=True,
    )

    class Meta:
        model = Rank
        fields = (
            "id",
            "name",
            "description",
            "required_experience",
            "icon",
            "color",
            "game_world_stories",
        )


class CompetencyNestedSerializer(serializers.ModelSerializer):
    """
    Компетенция. Вложенный сериалайзер.
    """

    game_world_stories = GameWorldStoryNestedSerializer(
        label=_("История игрового мира"),
        help_text=_("История игрового мира"),
        many=True,
    )

    class Meta:
        model = Competency
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "game_world_stories",
        )
