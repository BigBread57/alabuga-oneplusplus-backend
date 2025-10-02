import django_filters
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, T
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

    queryset = GameWorld.objects.defer("data_for_graph")
    filter_class = GameWorldListOrStatisticsOrStatisticsFilter


class GameWorldDataForGraphSelector(BaseSelector):
    """
    Игровой мир. Рейтинг. Селектор.
    """

    filter_class = GameWorldListOrStatisticsOrStatisticsFilter

    def get_queryset(self, **kwargs) -> QuerySet[T]:
        return GameWorld.objects.prefetch_related(
            "ranks__mission_branches__missions__game_world_stories",
            "ranks__mission_branches__missions__artifacts__game_world_stories",
            "ranks__mission_branches__missions__competencies__game_world_stories",
            "ranks__mission_branches__missions__mentor",
            "ranks__mission_branches__missions__category",
            "ranks__mission_branches__missions__level",
            "ranks__events__game_world_stories",
            "ranks__events__artifacts__game_world_stories",
            "ranks__events__competencies__game_world_stories",
            "ranks__events__mentor",
            "ranks__events__category",
        ).defer("data_for_graph")
