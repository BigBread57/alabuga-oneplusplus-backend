import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import EventCompetency


class EventCompetencyListFilterSerializer(serializers.Serializer):
    """
    Прокачка компетенций за событие. Список. Сериализатор для фильтра.
    """

    uuid = serializers.UUIDField(
        label=_("UUID"),
        help_text=_("UUID"),
        required=False,
    )
    event = serializers.IntegerField(
        label=_("Событие"),
        help_text=_("ID события"),
        required=False,
    )
    competency = serializers.IntegerField(
        label=_("Компетенция"),
        help_text=_("ID компетенции"),
        required=False,
    )


class EventCompetencyListFilter(django_filters.FilterSet):
    """
    Прокачка компетенций за событие. Список. Фильтр.
    """

    class Meta:
        model = EventCompetency
        fields = ("uuid", "event", "competency")


class EventCompetencyListSelector(BaseSelector):
    """
    Прокачка компетенций за событие. Список. Селектор.
    """

    queryset = EventCompetency.objects.select_related(
        "event",
        "competency",
    ).all()
    filter_class = EventCompetencyListFilter


class EventCompetencyDetailSelector(BaseSelector):
    """
    Прокачка компетенций за событие. Детальная информация. Селектор.
    """

    queryset = EventCompetency.objects.select_related(
        "event",
        "competency",
    )
    filter_class = EventCompetencyListFilter
