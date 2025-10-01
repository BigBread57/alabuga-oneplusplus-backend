from datetime import datetime, timedelta

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.models import Event


class EventListSerializer(serializers.ModelSerializer):
    """
    Событие. Список.
    """

    end_datetime = serializers.SerializerMethodField(
        label=_("Дата и время окончания события"),
        help_text=_("Дата и время окончания события"),
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "experience",
            "currency",
            "required_number",
            "start_datetime",
            "time_to_complete",
            "end_datetime",
        )

    def get_end_datetime(self, event: Event) -> datetime | None:
        """
        Дата и время окончания события.
        """
        if event.start_datetime and event.time_to_complete:
            return event.start_datetime + timedelta(hours=event.time_to_complete)
        return None


class EventDetailSerializer(serializers.ModelSerializer):
    """
    Событие. Детальная информация.
    """

    end_datetime = serializers.SerializerMethodField(
        label=_("Дата и время окончания события"),
        help_text=_("Дата и время окончания события"),
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "experience",
            "currency",
            "required_number",
            "start_datetime",
            "time_to_complete",
            "end_datetime",
        )

    def get_end_datetime(self, event: Event) -> datetime | None:
        """
        Дата и время окончания события.
        """
        if event.start_datetime and event.time_to_complete:
            return event.start_datetime + timedelta(hours=event.time_to_complete)
        return None


class EventCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Событие. Создание.
    """

    class Meta:
        model = Event
        fields = (
            "icon",
            "name",
            "description",
            "experience",
            "currency",
            "required_number",
            "is_active",
            "start_datetime",
            "time_to_complete",
            "category",
            "rank",
            "artifacts",
            "competencies",
            "game_world",
        )
