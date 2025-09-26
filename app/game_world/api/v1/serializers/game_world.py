from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

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


class GameWorldRatingSerializer(serializers.Serializer):
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

    character_missions = serializers.DictField(
        label=_("Информация по миссиям персонажа"),
        help_text=_("Информация по миссиям персонажа"),
    )
    character_events = serializers.DictField(
        label=_("Информация по событиям персонажей"),
        help_text=_("Информация по событиям персонажей"),
    )
