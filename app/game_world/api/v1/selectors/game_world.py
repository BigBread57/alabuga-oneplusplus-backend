import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import GameWorld


class GameWorldListOrRatingOrStatisticsFilterSerializer(serializers.Serializer):
    """
    Игровой мир. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class GameWorldListOrRatingOrStatisticsFilter(django_filters.FilterSet):
    """
    Игровой мир. Список. Фильтр.
    """

    class Meta:
        model = GameWorld
        fields = ("name",)


class GameWorldListOrRatingOrStatisticsSelector(BaseSelector):
    """
    Игровой мир. Рейтинг. Селектор.
    """

    queryset = GameWorld.objects.all()
    filter_class = GameWorldListOrRatingOrStatisticsFilter
