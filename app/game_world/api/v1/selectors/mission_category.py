import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import MissionCategory


class MissionCategoryListFilterSerializer(serializers.Serializer):
    """
    Категория миссии. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class MissionCategoryListFilter(django_filters.FilterSet):
    """
    Категория миссии. Список. Фильтр.
    """

    class Meta:
        model = MissionCategory
        fields = ("name",)


class MissionCategoryListSelector(BaseSelector):
    """
    Категория миссии. Список. Селектор.
    """

    queryset = MissionCategory.objects.all()
    filter_class = MissionCategoryListFilter


class MissionCategoryDetailSelector(BaseSelector):
    """
    Категория миссии. Детальная информация. Селектор.
    """

    queryset = MissionCategory.objects.all()
    filter_class = MissionCategoryListFilter
