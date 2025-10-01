import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, CurrentCharacterDefault
from user.models import CharacterCompetency


class CharacterCompetencyForCharacterFilterSerializer(serializers.Serializer):
    """
    Уровень компетенции персонажа. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class CharacterCompetencyOrDetailFilter(django_filters.FilterSet):
    """
    Уровень компетенции персонажа. Список. Фильтр.
    """

    class Meta:
        model = CharacterCompetency
        fields = ("character",)


class CharacterCompetencyListSelector(BaseSelector):
    """
    Уровень компетенции персонажа. Список. Селектор.
    """

    queryset = CharacterCompetency.objects.select_related(
        "character",
        "competency",
    ).order_by("is_received", "-experience", "-competency__level")
    filter_class = CharacterCompetencyOrDetailFilter


class CharacterCompetencyDetailSelector(BaseSelector):
    """
    Уровень компетенции персонажа. Детальная информация. Селектор.
    """

    queryset = CharacterCompetency.objects.select_related(
        "character",
        "competency",
    )
    filter_class = CharacterCompetencyOrDetailFilter
