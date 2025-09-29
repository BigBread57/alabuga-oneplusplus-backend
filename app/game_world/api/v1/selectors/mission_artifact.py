import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import MissionArtifact


class MissionArtifactListFilterSerializer(serializers.Serializer):
    """
    Артефакты за выполнение миссии. Список. Сериализатор для фильтра.
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
    artifact = serializers.IntegerField(
        label=_("Артефакт"),
        help_text=_("ID артефакта"),
        required=False,
    )


class MissionArtifactListFilter(django_filters.FilterSet):
    """
    Артефакты за выполнение миссии. Список. Фильтр.
    """

    class Meta:
        model = MissionArtifact
        fields = ("uuid", "mission", "artifact")


class MissionArtifactListSelector(BaseSelector):
    """
    Артефакты за выполнение миссии. Список. Селектор.
    """

    queryset = MissionArtifact.objects.select_related(
        "mission",
        "artifact",
    ).all()
    filter_class = MissionArtifactListFilter


class MissionArtifactDetailSelector(BaseSelector):
    """
    Артефакты за выполнение миссии. Детальная информация. Селектор.
    """

    queryset = MissionArtifact.objects.select_related(
        "mission",
        "artifact",
    )
    filter_class = MissionArtifactListFilter
