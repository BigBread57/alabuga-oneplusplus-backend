import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import GameWorld


class GameWorldListFilterSerializer(serializers.Serializer):
    """
    Игровой мир. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class GameWorldListFilter(django_filters.FilterSet):
    """
    Игровой мир. Список. Фильтр.
    """

    class Meta:
        model = GameWorld
        fields = ("name",)


class GameWorldListSelector(BaseSelector):
    """
    Игровой мир. Список. Селектор.
    """

    queryset = GameWorld.objects.all()
    filter_class = GameWorldListFilter


class GameWorldDetailSelector(BaseSelector):
    """
    Игровой мир. Детальная информация. Селектор.
    """

    queryset = GameWorld.objects.all()
    filter_class = GameWorldListFilter
