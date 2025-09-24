from rest_framework import serializers

from game_world.models import GameWorld, Artifact, Mission


class GameWorldNestedSerializer(serializers.ModelSerializer):
    """
    Игровой мир. Вложенный сериалайзер.
    """

    class Meta:
        model = GameWorld
        fields = (
            "id",
            "name",
            "description",
            "color",
            "currency_name",
        )

class ArtifactNestedSerializer(serializers.ModelSerializer):
    """
    Артефакт. Вложенный сериалайзер.
    """

    class Meta:
        model = Artifact
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "modifier",
            "modifier_value",
        )

class MissionNestedSerializer(serializers.ModelSerializer):
    """
    Миссия. Вложенный сериалайзер.
    """

    class Meta:
        model = Mission
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "experience",
            "currency",
            "order",
            "is_key_mission",
            "is_active",
            "time_to_complete",
            "branch",
            "level",
        )
