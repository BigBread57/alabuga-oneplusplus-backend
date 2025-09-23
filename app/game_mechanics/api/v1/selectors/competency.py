import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_mechanics.models import Competency
from game_world.models import GameWorld


class CompetencyListFilterSerializer(serializers.Serializer):
    """
    Компетенция. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )
    game_world = serializers.PrimaryKeyRelatedField(
        label=_("Игровой мир"),
        help_text=_("Игровой мир"),
        queryset=GameWorld.objects.all(),
        required=False,
    )


class CompetencyListFilter(django_filters.FilterSet):
    """
    Компетенция. Список. Фильтр.
    """

    class Meta:
        model = Competency
        fields = (
            "name",
            "game_world",
        )


class CompetencyListSelector(BaseSelector):
    """
    Компетенция. Список. Селектор.
    """

    queryset = Competency.objects.select_related(
        "game_world",
    ).all()
    filter_class = CompetencyListFilter
