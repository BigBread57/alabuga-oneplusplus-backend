from rest_framework import serializers

from app.game_world.models import MissionLevel


class MissionLevelListSerializer(serializers.ModelSerializer):
    """
    Урвоень миссии. Список.
    """

    class Meta:
        model = MissionLevel
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "multiplier_experience",
            "multiplier_currency",
        )


class MissionLevelDetailSerializer(serializers.ModelSerializer):
    """
    Урвоень миссии. Детальная информация.
    """

    class Meta:
        model = MissionLevel
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "multiplier_experience",
            "multiplier_currency",
        )


class MissionLevelCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Уровень миссии. Создание.
    """

    class Meta:
        model = MissionLevel
        fields = (
            "icon",
            "name",
            "description",
            "multiplier_experience",
            "multiplier_currency",
        )
