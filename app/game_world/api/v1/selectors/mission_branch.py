import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import MissionBranch


class MissionBranchListFilterSerializer(serializers.Serializer):
    """
    Ветка миссии. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class MissionBranchListFilter(django_filters.FilterSet):
    """
    Ветка миссии. Список. Фильтр.
    """

    class Meta:
        model = MissionBranch
        fields = ("name",)


class MissionBranchListSelector(BaseSelector):
    """
    Ветка миссии. Список. Селектор.
    """

    queryset = MissionBranch.objects.all()
    filter_class = MissionBranchListFilter


class MissionBranchDetailSelector(BaseSelector):
    """
    Ветка миссии. Детальная информация. Селектор.
    """

    queryset = MissionBranch.objects.all()
    filter_class = MissionBranchListFilter
