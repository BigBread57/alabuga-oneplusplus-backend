import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.common.selectors import BaseSelector
from app.game_world.models import Mission


class MissionListFilterSerializer(serializers.Serializer):
    """
    Миссия. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class MissionListFilter(django_filters.FilterSet):
    """
    Миссия. Список. Фильтр.
    """

    class Meta:
        model = Mission
        fields = ("name",)


class MissionListSelector(BaseSelector):
    """
    Миссия. Список. Селектор.
    """

    queryset = Mission.objects.all()
    filter_class = MissionListFilter


class MissionDetailSelector(BaseSelector):
    """
    Миссия. Детальная информация. Селектор.
    """

    queryset = Mission.objects.all()
    filter_class = MissionListFilter
