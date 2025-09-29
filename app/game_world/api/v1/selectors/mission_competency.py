import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import MissionCompetency


class MissionCompetencyListFilterSerializer(serializers.Serializer):
    """
    Прокачка компетенций за миссию. Список. Сериализатор для фильтра.
    """

    uuid = serializers.UUIDField(
        label=_("UUID"),
        help_text=_("UUID"),
        required=False,
    )
    mission = serializers.IntegerField(
        label=_("Миссия"),
        help_text=_("ID миссии"),
        required=False,
    )
    competency = serializers.IntegerField(
        label=_("Компетенция"),
        help_text=_("ID компетенции"),
        required=False,
    )


class MissionCompetencyListFilter(django_filters.FilterSet):
    """
    Прокачка компетенций за миссию. Список. Фильтр.
    """

    class Meta:
        model = MissionCompetency
        fields = ("uuid", "mission", "competency")


class MissionCompetencyListSelector(BaseSelector):
    """
    Прокачка компетенций за миссию. Список. Селектор.
    """

    queryset = MissionCompetency.objects.select_related(
        "mission",
        "competency",
    ).all()
    filter_class = MissionCompetencyListFilter


class MissionCompetencyDetailSelector(BaseSelector):
    """
    Прокачка компетенций за миссию. Детальная информация. Селектор.
    """

    queryset = MissionCompetency.objects.select_related(
        "mission",
        "competency",
    )
    filter_class = MissionCompetencyListFilter
