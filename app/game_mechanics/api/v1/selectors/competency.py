import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.common.selectors import BaseSelector
from app.game_mechanics.models import Competency


class CompetencyListFilterSerializer(serializers.Serializer):
    """
    Компетенция. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название категории"),
        help_text=_("Название категории"),
        required=False,
    )

class CompetencyListFilter(django_filters.FilterSet):
    """
    Компетенция. Список. Фильтр.
    """

    class Meta:
        model = Competency
        fields = (
            "name",
        )


class CompetencyListSelector(BaseSelector):
    """
    Компетенция. Список. Селектор.
    """

    queryset = Competency.objects.all()
    filter_class = CompetencyListFilter
