import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, CurrentCharacterDefault
from game_world.models import MissionBranch
from user.models import CharacterMission, CharacterMissionBranch


class CharacterMissionBranchListFilterSerializer(serializers.Serializer):
    """
    Ветка миссий персонажа. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )
    branch = serializers.PrimaryKeyRelatedField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        queryset=MissionBranch.objects.all(),
        required=False,
    )
    status = serializers.ChoiceField(
        label=_("Статус пользовательской миссии"),
        help_text=_("Статус пользовательской миссии"),
        choices=CharacterMission.Statuses.choices,
        required=False,
    )


class CharacterMissionBranchListFilter(django_filters.FilterSet):
    """
    Ветка миссий персонажа. Список. Фильтр.
    """

    status = django_filters.CharFilter(
        label=_("Статус пользовательской миссии"),
        help_text=_("Статус пользовательской миссии"),
        field_name="character_missions__status",
        distinct=True,
    )

    class Meta:
        model = CharacterMissionBranch
        fields = (
            "character",
            "branch",
            "status",
        )


class CharacterMissionBranchListSelector(BaseSelector):
    """
    Ветка миссий персонажа. Список. Селектор.
    """

    queryset = CharacterMissionBranch.objects.select_related(
        "branch",
    ).prefetch_related(
        "character_missions",
    )
    filter_class = CharacterMissionBranchListFilter
