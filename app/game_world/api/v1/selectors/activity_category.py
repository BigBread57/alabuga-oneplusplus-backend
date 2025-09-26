import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import ActivityCategory


class ActivityCategoryListFilterSerializer(serializers.Serializer):
    """
    Категория миссии. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class ActivityCategoryListFilter(django_filters.FilterSet):
    """
    Категория миссии. Список. Фильтр.
    """

    class Meta:
        model = ActivityCategory
        fields = ("name",)


class ActivityCategoryListSelector(BaseSelector):
    """
    Категория миссии. Список. Селектор.
    """

    queryset = ActivityCategory.objects.all()
    filter_class = ActivityCategoryListFilter


class ActivityCategoryDetailSelector(BaseSelector):
    """
    Категория миссии. Детальная информация. Селектор.
    """

    queryset = ActivityCategory.objects.all()
    filter_class = ActivityCategoryListFilter
