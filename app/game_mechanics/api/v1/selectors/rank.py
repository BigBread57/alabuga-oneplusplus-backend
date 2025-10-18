import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_mechanics.models import Rank
from game_world.models import GameWorld


class RankListFilterSerializer(serializers.Serializer):
    """
    Ранг. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )
    parent = serializers.PrimaryKeyRelatedField(
        label=_("Родительский ранг"),
        help_text=_("Родительский ранг"),
        queryset=Rank.objects.all(),
        required=False,
    )
    game_world = serializers.PrimaryKeyRelatedField(
        label=_("Игровой мир"),
        help_text=_("Игровой мир"),
        queryset=GameWorld.objects.defer("data_for_graph"),
        required=False,
    )


class RankListFilter(django_filters.FilterSet):
    """
    Ранг. Список. Фильтр.
    """

    class Meta:
        model = Rank
        fields = (
            "name",
            "parent",
            "game_world",
        )


class RankListSelector(BaseSelector):
    """
    Ранг. Список. Селектор.
    """

    queryset = Rank.objects.select_related("game_world", "parent")
    filter_class = RankListFilter
