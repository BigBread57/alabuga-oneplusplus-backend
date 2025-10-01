from rest_framework import serializers

from game_world.models import Mission


class MissionListSerializer(serializers.ModelSerializer):
    """
    Миссия. Список.
    """

    class Meta:
        model = Mission
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "branch",
            "experience",
            "currency",
            "order",
            "is_key_mission",
            "is_active",
            "time_to_complete",
            "level",
            "artifacts",
            "competencies",
            "game_world",
        )


class MissionDetailSerializer(serializers.ModelSerializer):
    """
    Миссия. Детальная информация.
    """

    class Meta:
        model = Mission
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "branch",
            "experience",
            "currency",
            "order",
            "is_key_mission",
            "is_active",
            "time_to_complete",
            "level",
            "artifacts",
            "competencies",
            "game_world",
        )


class MissionCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Миссия. Создание.
    """

    class Meta:
        model = Mission
        fields = (
            "icon",
            "name",
            "description",
            "branch",
            "experience",
            "currency",
            "order",
            "is_key_mission",
            "is_active",
            "time_to_complete",
            "level",
            "artifacts",
            "competencies",
            "game_world",
        )
