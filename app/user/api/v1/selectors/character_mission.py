import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from common.constants import CharacterRoles
from common.selectors import BaseSelector, CurrentCharacterDefault
from game_world.models import MissionBranch
from user.models import CharacterMission, User


class CharacterMissionListFilterSerializer(serializers.Serializer):
    """
    Миссия персонажа. Список. Сериализатор для фильтра.
    """

    status = serializers.ChoiceField(
        label=_("Статус"),
        help_text=_("Статус"),
        choices=CharacterMission.Statuses.choices,
        required=True,
    )
    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class CharacterMissionDetailOrUpdateFilterSerializer(serializers.Serializer):
    """
    Миссия персонажа. Детальная информация/изменение со стороны персонажа. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class CharacterMissionForInspectorFilterSerializer(serializers.Serializer):
    """
    Миссия персонажа. Детальная информация/изменение со стороны проверяющего. Сериализатор для фильтра.
    """

    inspector = serializers.HiddenField(
        label=_("Проверяющий"),
        help_text=_("Проверяющий"),
        default=CurrentUserDefault(),
    )


class CharacterMissionListFilter(django_filters.FilterSet):
    """
    Миссия персонажа. Список. Фильтр.
    """

    class Meta:
        model = CharacterMission
        fields = ("status", "character")


class CharacterMissionDetailOrUpdateFilter(django_filters.FilterSet):
    """
    Миссия персонажа. Детальная информация/изменение со стороны персонажа. Фильтр.
    """

    class Meta:
        model = CharacterMission
        fields = ("character",)


class CharacterMissionDetailForInspectorFilter(django_filters.FilterSet):
    """
    Миссия персонажа. Детальная информация/изменение со стороны проверяющего. Фильтр.
    """

    inspector = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Проверяющий"),
        help_text=_("Проверяющий"),
        method="inspector_filter",
    )

    class Meta:
        model = CharacterMission
        fields = ("inspector",)

    def inspector_filter(self, queryset, name, value):
        """
        Фильтр по проверяющему.
        """
        if getattr(value, "role", None) == CharacterRoles.HR:
            return queryset.all()
        return queryset.filter(inspector=value)


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


class CharacterMissionBranchListSelector(BaseSelector):
    """
    Ветка миссии персонаж. Список. Селектор.
    """

    queryset = MissionBranch.objects.select_related(
        "missions__character_missions",
    )


class CharacterMissionDetailSelector(BaseSelector):
    """
    Миссия персонажа. Детальная информация. Селектор.
    """

    queryset = CharacterMission.objects.select_related(
        "character",
        "mission",
        "inspector",
    )
    filter_class = CharacterMissionDetailOrUpdateFilter


class CharacterMissionUpdateFromCharacterSelector(BaseSelector):
    """
    Миссия персонажа. Изменение со стороны персонажа. Селектор.
    """

    queryset = CharacterMission.objects.all()
    filter_class = CharacterMissionDetailOrUpdateFilter


class CharacterMissionUpdateFromInspectorSelector(BaseSelector):
    """
    Миссия персонажа. Изменение со стороны проверяющего. Селектор.
    """

    queryset = CharacterMission.objects.all()
    filter_class = CharacterMissionDetailOrUpdateFilter
