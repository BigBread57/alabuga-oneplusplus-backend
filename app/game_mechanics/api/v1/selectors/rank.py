import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.common.selectors import BaseSelector
from app.game_mechanics.models import Rank


class RankListFilterSerializer(serializers.Serializer):
    """
    Ранг. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )
    order = serializers.IntegerField(
        label=_("Порядок ранга"),
        help_text=_("Порядок ранга"),
        required=False,
    )


class RankListFilter(django_filters.FilterSet):
    """
    Ранг. Список. Фильтр.
    """

    class Meta:
        model = Rank
        fields = (
            "name",
            "order",
        )


class RankListSelector(BaseSelector):
    """
    Ранг. Список. Селектор.
    """

    queryset = Rank.objects.all()
    filter_class = RankListFilter
