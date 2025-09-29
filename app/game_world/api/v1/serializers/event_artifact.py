from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.models import EventArtifact


class EventArtifactListSerializer(serializers.ModelSerializer):
    """
    Артефакты за выполнение события. Список.
    """

    event_name = serializers.CharField(
        source="event.name",
        label=_("Название события"),
        read_only=True,
    )
    artifact_name = serializers.CharField(
        source="artifact.name",
        label=_("Название артефакта"),
        read_only=True,
    )

    class Meta:
        model = EventArtifact
        fields = (
            "id",
            "uuid",
            "event",
            "event_name",
            "artifact",
            "artifact_name",
        )


class EventArtifactDetailSerializer(serializers.ModelSerializer):
    """
    Артефакты за выполнение события. Детальная информация.
    """

    event_name = serializers.CharField(
        source="event.name",
        label=_("Название события"),
        read_only=True,
    )
    artifact_name = serializers.CharField(
        source="artifact.name",
        label=_("Название артефакта"),
        read_only=True,
    )

    class Meta:
        model = EventArtifact
        fields = (
            "id",
            "uuid",
            "event",
            "event_name",
            "artifact",
            "artifact_name",
        )


class EventArtifactCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Артефакты за выполнение события. Создание/изменение.
    """

    class Meta:
        model = EventArtifact
        fields = (
            "event",
            "artifact",
        )
