from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.models import MissionArtifact


class MissionArtifactListSerializer(serializers.ModelSerializer):
    """
    Артефакты за выполнение миссии. Список.
    """

    mission_name = serializers.CharField(
        source="mission.name",
        label=_("Название миссии"),
        read_only=True,
    )
    artifact_name = serializers.CharField(
        source="artifact.name",
        label=_("Название артефакта"),
        read_only=True,
    )

    class Meta:
        model = MissionArtifact
        fields = (
            "id",
            "uuid",
            "mission",
            "mission_name",
            "artifact",
            "artifact_name",
        )


class MissionArtifactDetailSerializer(serializers.ModelSerializer):
    """
    Артефакты за выполнение миссии. Детальная информация.
    """

    mission_name = serializers.CharField(
        source="mission.name",
        label=_("Название миссии"),
        read_only=True,
    )
    artifact_name = serializers.CharField(
        source="artifact.name",
        label=_("Название артефакта"),
        read_only=True,
    )

    class Meta:
        model = MissionArtifact
        fields = (
            "id",
            "uuid",
            "mission",
            "mission_name",
            "artifact",
            "artifact_name",
        )


class MissionArtifactCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Артефакты за выполнение миссии. Создание/изменение.
    """

    class Meta:
        model = MissionArtifact
        fields = (
            "mission",
            "artifact",
        )
