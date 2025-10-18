import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, CurrentCharacterDefault
from game_world.models import MissionBranch
from user.models import Character, CharacterMission


class CharacterMissionForCharacterFilterSerializer(serializers.Serializer):
    """
    Миссия персонажа. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class CharacterMissionListFilterSerializer(serializers.Serializer):
    """
    Миссия персонажа. Список. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )
    status = serializers.ChoiceField(
        label=_("Статус"),
        help_text=_("Статус"),
        choices=CharacterMission.Statuses.choices,
        required=True,
    )
    branch = serializers.PrimaryKeyRelatedField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        queryset=MissionBranch.objects.all(),
        required=False,
    )


class CharacterMissionListForInspectorFilterSerializer(serializers.Serializer):
    """
    Миссия персонажа для проверябщего. Сериализатор для фильтра.
    """

    character = serializers.PrimaryKeyRelatedField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        queryset=Character.objects.all(),
        required=False,
    )
    status = serializers.ChoiceField(
        label=_("Статус"),
        help_text=_("Статус"),
        choices=CharacterMission.Statuses.choices,
        required=True,
    )
    branch = serializers.PrimaryKeyRelatedField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        queryset=MissionBranch.objects.all(),
        required=False,
    )


class CharacterMissionListFilter(django_filters.FilterSet):
    """
    Миссия персонажа. Список. Фильтр.
    """

    class Meta:
        model = CharacterMission
        fields = (
            "status",
            "character",
            "branch",
        )


class CharacterMissionListSelector(BaseSelector):
    """
    Миссия персонажа. Список. Селектор.
    """

    queryset = CharacterMission.objects.select_related(
        "character",
        "mission",
        "inspector",
    )
    filter_class = CharacterMissionListFilter


class CharacterMissionListForInspectorSelector(BaseSelector):
    """
    Событие персонажа для проверяющего. Селектор.
    """

    filter_class = CharacterMissionListFilter

    def get_queryset(self, **kwargs) -> models.QuerySet:
        active_character = self.request.user.active_character
        return CharacterMission.objects.select_related(
            "character",
            "mission",
            "inspector",
        ).exclude(
            character=active_character,
        )
