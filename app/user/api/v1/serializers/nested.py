from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.api.v1.serializers.nested import CompetencyNestedSerializer, RankNestedSerializer
from game_world.api.v1.serializers.nested import ArtifactNestedSerializer, MissionNestedSerializer, \
    EventNestedSerializer
from user.models import CharacterArtifact, CharacterCompetency, CharacterEvent, CharacterMission, User
from user.models.character_rank import CharacterRank


class UserNestedSerializer(serializers.ModelSerializer):
    """
    Пользователь. Вложенный сериалайзер.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
        )


class CharacterArtifactNestedSerializer(serializers.ModelSerializer):
    """
    Артефакты персонажа. Вложенный сериалайзер.
    """

    artifact = ArtifactNestedSerializer(
        label=_("Артефакты"),
        help_text=_("Артефакты"),
    )

    class Meta:
        model = CharacterArtifact
        fields = (
            "id",
            "artifact",
            "created_at",
        )


class CharacterCompetencyNestedSerializer(serializers.ModelSerializer):
    """
    Уровень компетенции персонажа. Вложенный сериалайзер.
    """

    competency = CompetencyNestedSerializer(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
    )

    class Meta:
        model = CharacterCompetency
        fields = (
            "id",
            "competency",
            "experience",
        )


class CharacterRankNestedSerializer(serializers.ModelSerializer):
    """
    Ранг персонажа. Вложенный сериалайзер.
    """

    rank = RankNestedSerializer(
        label=_("Ранг"),
        help_text=_("Ранг"),
    )

    class Meta:
        model = CharacterRank
        fields = (
            "id",
            "rank",
            "experience",
        )

class CharacterMissionNestedSerializer(serializers.ModelSerializer):
    """
    Прогресс персонажа по миссиям. Вложенный сериалайзер.
    """

    mission = MissionNestedSerializer(
        label=_("Миссия"),
        help_text=_("Миссия"),
    )

    class Meta:
        model = CharacterMission
        fields = (
            "id",
            "status",
            "start_datetime",
            "end_datetime",
            "result",
            "mission",
            "inspector",
            "inspector_comment",
        )


class CharacterEventNestedSerializer(serializers.ModelSerializer):
    """
    Прогресс персонажа по событиям. Вложенный сериалайзер.
    """

    event = EventNestedSerializer(
        label=_("Событие"),
        help_text=_("Событие"),
    )
    status_display_name = serializers.SerializerMethodField(
        label=_("Название статуса"),
        help_text=_("Название статуса"),
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
        )
