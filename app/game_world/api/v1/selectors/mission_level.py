import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.common.selectors import BaseSelector
from app.game_world.models import MissionLevel


class MissionLevelListFilterSerializer(serializers.Serializer):
    """
    Уровень миссии. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class MissionLevelListFilter(django_filters.FilterSet):
    """
    Уровень миссии. Список. Фильтр.
    """

    class Meta:
        model = MissionLevel
        fields = ("name",)


class MissionLevelListSelector(BaseSelector):
    """
    Уровень миссии. Список. Селектор.
    """

    queryset = MissionLevel.objects.all()
    filter_class = MissionLevelListFilter


class MissionLevelDetailSelector(BaseSelector):
    """
    Уровень миссии. Детальная информация. Селектор.
    """

    queryset = MissionLevel.objects.all()
    filter_class = MissionLevelListFilter
