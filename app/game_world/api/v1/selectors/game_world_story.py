import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import GameWorldStory


class GameWorldStoryListFilterSerializer(serializers.Serializer):
    """
    История игрового мира. Список. Сериализатор для фильтра.
    """

    uuid = serializers.UUIDField(
        label=_("UUID"),
        help_text=_("UUID"),
        required=False,
    )
    game_world = serializers.IntegerField(
        label=_("Игровой мир"),
        help_text=_("ID игрового мира"),
        required=False,
    )


class GameWorldStoryListFilter(django_filters.FilterSet):
    """
    История игрового мира. Список. Фильтр.
    """

    class Meta:
        model = GameWorldStory
        fields = ("uuid", "game_world")


class GameWorldStoryListSelector(BaseSelector):
    """
    История игрового мира. Список. Селектор.
    """

    queryset = GameWorldStory.objects.select_related(
        "game_world",
        "content_type",
    ).all()
    filter_class = GameWorldStoryListFilter


class GameWorldStoryDetailSelector(BaseSelector):
    """
    История игрового мира. Детальная информация. Селектор.
    """

    queryset = GameWorldStory.objects.select_related(
        "game_world",
        "content_type",
    )
    filter_class = GameWorldStoryListFilter
