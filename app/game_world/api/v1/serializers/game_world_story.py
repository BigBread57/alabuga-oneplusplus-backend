from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.models import GameWorldStory


class GameWorldStoryListSerializer(serializers.ModelSerializer):
    """
    История игрового мира. Список.
    """

    game_world_name = serializers.CharField(
        source="game_world.name",
        label=_("Название игрового мира"),
        read_only=True,
    )

    class Meta:
        model = GameWorldStory
        fields = (
            "id",
            "uuid",
            "image",
            "text",
            "game_world",
            "game_world_name",
        )


class GameWorldStoryDetailSerializer(serializers.ModelSerializer):
    """
    История игрового мира. Детальная информация.
    """

    game_world_name = serializers.CharField(
        source="game_world.name",
        label=_("Название игрового мира"),
        read_only=True,
    )

    class Meta:
        model = GameWorldStory
        fields = (
            "id",
            "uuid",
            "image",
            "text",
            "game_world",
            "game_world_name",
            "content_type",
            "object_id",
        )


class GameWorldStoryCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    История игрового мира. Создание/изменение.
    """

    class Meta:
        model = GameWorldStory
        fields = (
            "image",
            "text",
            "game_world",
        )
