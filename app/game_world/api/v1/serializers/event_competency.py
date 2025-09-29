from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.models import EventCompetency


class EventCompetencyListSerializer(serializers.ModelSerializer):
    """
    Прокачка компетенций за событие. Список.
    """

    event_name = serializers.CharField(
        source="event.name",
        label=_("Название события"),
        read_only=True,
    )
    competency_name = serializers.CharField(
        source="competency.name",
        label=_("Название компетенции"),
        read_only=True,
    )

    class Meta:
        model = EventCompetency
        fields = (
            "id",
            "uuid",
            "event",
            "event_name",
            "competency",
            "competency_name",
            "experience",
        )


class EventCompetencyDetailSerializer(serializers.ModelSerializer):
    """
    Прокачка компетенций за событие. Детальная информация.
    """

    event_name = serializers.CharField(
        source="event.name",
        label=_("Название события"),
        read_only=True,
    )
    competency_name = serializers.CharField(
        source="competency.name",
        label=_("Название компетенции"),
        read_only=True,
    )

    class Meta:
        model = EventCompetency
        fields = (
            "id",
            "uuid",
            "event",
            "event_name",
            "competency",
            "competency_name",
            "experience",
        )


class EventCompetencyCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Прокачка компетенций за событие. Создание/изменение.
    """

    class Meta:
        model = EventCompetency
        fields = (
            "event",
            "competency",
            "experience",
        )
