from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.api.v1.serializers.nested import EventNestedSerializer
from user.models import CharacterEvent


class CharacterEventListSerializer(serializers.ModelSerializer):
    """
    Событие персонажа. Список.
    """

    event = EventNestedSerializer(
        label=_("Событие"),
        help_text=_("Событие"),
    )
    status_display_name = serializers.SerializerMethodField(
        label=_("Название статуса"),
        help_text=_("Название статуса"),
    )
    content_type_id = serializers.IntegerField(
        label=_("ID тип содержимого"),
        help_text=_("ID тип содержимого"),
    )

    class Meta:
        model = CharacterEvent
        fields = (
            "id",
            "status",
            "status_display_name",
            "start_datetime",
            "end_datetime",
            "content_type_id",
            "event",
        )

    def get_status_display_name(self, character_event: CharacterEvent) -> str:
        """
        Название статуса.
        """
        return character_event.get_status_display()


class CharacterEventDetailSerializer(serializers.ModelSerializer):
    """
    Событие персонажа. Детальная информация.
    """

    event = EventNestedSerializer(
        label=_("Событие"),
        help_text=_("Событие"),
    )
    status_display_name = serializers.SerializerMethodField(
        label=_("Название статуса"),
        help_text=_("Название статуса"),
    )
    content_type_id = serializers.IntegerField(
        label=_("ID тип содержимого"),
        help_text=_("ID тип содержимого"),
    )

    class Meta:
        model = CharacterEvent
        fields = (
            "id",
            "status",
            "status_display_name",
            "start_datetime",
            "end_datetime",
            "event",
            "inspector",
            "inspector_comment",
            "result",
            "content_type_id",
        )

    def get_status_display_name(self, character_event: CharacterEvent) -> str:
        """
        Название статуса.
        """
        return character_event.get_status_display()


class CharacterEventUpdateFromCharacterSerializer(serializers.ModelSerializer):
    """
    Миссия персонажа. Изменение со стороны персонажа.
    """

    class Meta:
        model = CharacterEvent
        fields = ("result",)


class CharacterEventUpdateFromInspectorSerializer(serializers.ModelSerializer):
    """
    Миссия персонажа. Изменение со стороны персонажа.
    """

    class Meta:
        model = CharacterEvent
        fields = (
            "status",
            "inspector_comment",
        )
