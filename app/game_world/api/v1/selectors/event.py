import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.common.selectors import BaseSelector
from app.game_world.models import Event


class EventListFilterSerializer(serializers.Serializer):
    """
    Событие. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class EventListFilter(django_filters.FilterSet):
    """
    Событие. Список. Фильтр.
    """

    class Meta:
        model = Event
        fields = ("name",)


class EventListSelector(BaseSelector):
    """
    Событие. Список. Селектор.
    """

    queryset = Event.objects.select_related(
        "rank",
        "competency",
    ).all()
    filter_class = EventListFilter


class EventDetailSelector(BaseSelector):
    """
    Событие. Детальная информация. Селектор.
    """

    queryset = (
        Event.objects.select_related(
            "category",
            "rank",
            "game_world",
        )
        .prefetch_related(
            "artifacts",
            "competencies",
        )
        .filter(
            is_active=True,
        )
    )
    filter_class = EventListFilter
