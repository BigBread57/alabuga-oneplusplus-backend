from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.models import ActivityCategory, Artifact, Event, GameWorld, Mission, MissionBranch


class GameWorldNestedSerializer(serializers.ModelSerializer):
    """
    Игровой мир. Вложенный сериалайзер.
    """

    class Meta:
        model = GameWorld
        fields = (
            "id",
            "name",
            "description",
            "color",
            "currency_name",
        )


class ArtifactNestedSerializer(serializers.ModelSerializer):
    """
    Артефакт. Вложенный сериалайзер.
    """

    class Meta:
        model = Artifact
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "modifier",
            "modifier_value",
        )


class ActivityCategoryNestedSerializer(serializers.ModelSerializer):
    """
    Категория активности. Вложенный сериалайзер.
    """

    class Meta:
        model = ActivityCategory
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
        )


class MissionBranchNestedSerializer(serializers.ModelSerializer):
    """
    Ветка миссий. Вложенный сериалайзер.
    """

    category = ActivityCategoryNestedSerializer(
        label=_("Ветка миссий"),
        help_text=_("Ветка миссий"),
    )

    class Meta:
        model = MissionBranch
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "category",
        )


class MissionNestedSerializer(serializers.ModelSerializer):
    """
    Миссия. Вложенный сериалайзер.
    """

    branch = MissionBranchNestedSerializer(
        label=_("Ветка миссий"),
        help_text=_("Ветка миссий"),
    )

    class Meta:
        model = Mission
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "order",
            "experience",
            "currency",
            "is_key_mission",
            "level",
            "branch",
        )


class EventNestedSerializer(serializers.ModelSerializer):
    """
    Событие. Вложенный сериалайзер.
    """

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "currency",
            "experience",
            "category",
        )
