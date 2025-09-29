from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.models import MissionCompetency


class MissionCompetencyListSerializer(serializers.ModelSerializer):
    """
    Прокачка компетенций за миссию. Список.
    """

    mission_name = serializers.CharField(
        source="mission.name",
        label=_("Название миссии"),
        read_only=True,
    )
    competency_name = serializers.CharField(
        source="competency.name",
        label=_("Название компетенции"),
        read_only=True,
    )

    class Meta:
        model = MissionCompetency
        fields = (
            "id",
            "uuid",
            "mission",
            "mission_name",
            "competency",
            "competency_name",
            "experience",
        )


class MissionCompetencyDetailSerializer(serializers.ModelSerializer):
    """
    Прокачка компетенций за миссию. Детальная информация.
    """

    mission_name = serializers.CharField(
        source="mission.name",
        label=_("Название миссии"),
        read_only=True,
    )
    competency_name = serializers.CharField(
        source="competency.name",
        label=_("Название компетенции"),
        read_only=True,
    )

    class Meta:
        model = MissionCompetency
        fields = (
            "id",
            "uuid",
            "mission",
            "mission_name",
            "competency",
            "competency_name",
            "experience",
        )


class MissionCompetencyCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Прокачка компетенций за миссию. Создание/изменение.
    """

    class Meta:
        model = MissionCompetency
        fields = (
            "mission",
            "competency",
            "experience",
        )
