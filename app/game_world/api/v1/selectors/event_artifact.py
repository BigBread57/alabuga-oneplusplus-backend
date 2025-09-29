import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import EventArtifact


class EventArtifactListFilterSerializer(serializers.Serializer):
    """
    Артефакты за выполнение события. Список. Сериализатор для фильтра.
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
    artifact = serializers.IntegerField(
        label=_("Артефакт"),
        help_text=_("ID артефакта"),
        required=False,
    )


class EventArtifactListFilter(django_filters.FilterSet):
    """
    Артефакты за выполнение события. Список. Фильтр.
    """

    class Meta:
        model = EventArtifact
        fields = ("uuid", "event", "artifact")


class EventArtifactListSelector(BaseSelector):
    """
    Артефакты за выполнение события. Список. Селектор.
    """

    queryset = EventArtifact.objects.select_related(
        "event",
        "artifact",
    ).all()
    filter_class = EventArtifactListFilter


class EventArtifactDetailSelector(BaseSelector):
    """
    Артефакты за выполнение события. Детальная информация. Селектор.
    """

    queryset = EventArtifact.objects.select_related(
        "event",
        "artifact",
    )
    filter_class = EventArtifactListFilter
