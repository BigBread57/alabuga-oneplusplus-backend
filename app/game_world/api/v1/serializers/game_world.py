from rest_framework import serializers

from app.game_world.models import GameWorld


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
