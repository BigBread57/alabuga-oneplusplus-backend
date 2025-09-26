from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.api.v1.serializers.nested import MissionNestedSerializer
from user.models import CharacterMission


class CharacterMissionListSerializer(serializers.ModelSerializer):
    """
    Миссия персонажа. Список.
    """

    mission = MissionNestedSerializer(
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
        model = CharacterMission
        fields = (
            "id",
            "status",
            "status_display_name",
            "start_datetime",
            "end_datetime",
            "mission",
            "content_type_id",
        )

    def get_status_display_name(self, character_mission: CharacterMission) -> str:
        """
        Название статуса.
        """
        return character_mission.get_status_display()


class CharacterMissionDetailSerializer(serializers.ModelSerializer):
    """
    Миссия персонажа. Детальная информация.
    """

    mission = MissionNestedSerializer(
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
        model = CharacterMission
        fields = (
            "id",
            "status",
            "status_display_name",
            "start_datetime",
            "end_datetime",
            "character",
            "mission",
            "inspector",
            "inspector_comment",
            "result",
            "content_type_id",
        )

    def get_status_display_name(self, character_mission: CharacterMission) -> str:
        """
        Название статуса.
        """
        return character_mission.get_status_display()


class CharacterMissionUpdateFromCharacterSerializer(serializers.ModelSerializer):
    """
    Событие персонажа. Изменение со стороны персонажа.
    """

    class Meta:
        model = CharacterMission
        fields = ("result",)


class CharacterMissionUpdateFromInspectorSerializer(serializers.ModelSerializer):
    """
    Событие персонажа. Изменение со стороны персонажа.
    """

    class Meta:
        model = CharacterMission
        fields = (
            "status",
            "inspector_comment",
        )
