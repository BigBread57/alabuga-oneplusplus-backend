import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_mechanics.api.v1.serializers.nested import RankNestedSerializer
from game_world.models import GameWorld


class GameWorldListOrStatisticsOrStatisticsFilterSerializer(serializers.Serializer):
    """
    Игровой мир. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class GameWorldListOrStatisticsOrStatisticsFilter(django_filters.FilterSet):
    """
    Игровой мир. Список. Фильтр.
    """

    class Meta:
        model = GameWorld
        fields = ("name",)


class GameWorldListOrStatisticsOrStatisticsSelector(BaseSelector):
    """
    Игровой мир. Рейтинг. Селектор.
    """

    queryset = GameWorld.objects.all()
    filter_class = GameWorldListOrStatisticsOrStatisticsFilter


class GameWorldListWithAllEntitiesSelector(BaseSelector):
    """
    Игровой мир. Рейтинг. Селектор.
    """

    ranks = RankNestedSerializer

    queryset = GameWorld.objects.prefetch_related(
        "ranks__mission_branches__missions__artifacts",
        "ranks__mission_branches__missions__competencies",
        "ranks__mission_branches__missions__required_missions",
        "ranks__mission_branches__missions__mentor",
        "ranks__mission_branches__missions__category",
        "ranks__mission_branches__missions__level",
        "ranks__events__artifacts",
        "ranks__events__competencies",
        "ranks__events__mentor",
        "ranks__events__category",
    )
    filter_class = GameWorldListOrStatisticsOrStatisticsFilter
