from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.api.v1.serializers.nested import MissionNestedSerializer
from multimedia.api.v1.serializers.nested import MultimediaNestedSerializer
from user.api.v1.serializers.nested import CharacterNestedSerializer
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


class CharacterMissionListForInspectorSerializer(serializers.ModelSerializer):
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
    character = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
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
            "character",
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
    multimedia = MultimediaNestedSerializer(
        label=_("Мультимедиа"),
        help_text=_("Мультимедиа"),
        many=True,
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
            "multimedia",
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


class CharacterMissionUpdateForInspectorSerializer(serializers.ModelSerializer):
    """
    Событие персонажа. Изменение со стороны персонажа.
    """

    class Meta:
        model = CharacterMission
        fields = (
            "status",
            "inspector_comment",
        )
