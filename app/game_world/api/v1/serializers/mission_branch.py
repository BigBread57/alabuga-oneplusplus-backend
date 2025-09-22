from rest_framework import serializers

from app.game_world.models import MissionBranch


class MissionBranchListSerializer(serializers.ModelSerializer):
    """
    Ветка миссии. Список.
    """

    class Meta:
        model = MissionBranch
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "color",
            "is_active",
            "start_datetime",
            "time_to_complete",
            "rank",
            "category",
            "mentor",
            "game_world",
        )


class MissionBranchDetailSerializer(serializers.ModelSerializer):
    """
    Ветка миссии. Детальная информация.
    """

    class Meta:
        model = MissionBranch
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "color",
            "is_active",
            "start_datetime",
            "time_to_complete",
            "rank",
            "category",
            "mentor",
            "game_world",
        )


class MissionBranchCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Ветка миссии. Создание.
    """

    class Meta:
        model = MissionBranch
        fields = (
            "icon",
            "name",
            "description",
            "color",
            "is_active",
            "start_datetime",
            "time_to_complete",
            "rank",
            "category",
            "mentor",
            "game_world",
        )
