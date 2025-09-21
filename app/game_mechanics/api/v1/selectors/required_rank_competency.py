import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.common.selectors import BaseSelector
from app.game_mechanics.models import RequiredRankCompetency, Rank, Competency


class RequiredRankCompetencyListFilterSerializer(serializers.Serializer):
    """
    Ранг. Список. Сериализатор для фильтра.
    """

    rank = serializers.PrimaryKeyRelatedField(
        label=_("Ранг"),
        help_text=_("Ранг"),
        queryset=Rank.objects.all(),
        required=False,
    )
    competency = serializers.PrimaryKeyRelatedField(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
        queryset=Competency.objects.all(),
        required=False,
    )


class RequiredRankCompetencyListFilter(django_filters.FilterSet):
    """
    Ранг. Список. Фильтр.
    """

    class Meta:
        model = RequiredRankCompetency
        fields = (
            "rank",
            "competency",
        )


class RequiredRankCompetencyListSelector(BaseSelector):
    """
    Ранг. Список. Селектор.
    """

    queryset = RequiredRankCompetency.objects.all()
    filter_class = RequiredRankCompetencyListFilter
