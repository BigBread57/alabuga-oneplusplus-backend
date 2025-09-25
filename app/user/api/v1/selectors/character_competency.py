import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, CurrentCharacterDefault
from user.models import CharacterCompetency


class CharacterCompetencyListOrDetailFilterSerializer(serializers.Serializer):
    """
    Уровень компетенции персонажа. Список. Сериализатор для фильтра.
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
        fields = (
            "character",
        )

class CharacterCompetencyListSelector(BaseSelector):
    """
    Уровень компетенции персонажа. Список. Селектор.
    """

    queryset = CharacterCompetency.objects.select_related(
        "character",
        "Competency",
        "inspector",
    )
    filter_class = CharacterCompetencyOrDetailFilter


class CharacterCompetencyDetailSelector(BaseSelector):
    """
    Уровень компетенции персонажа. Детальная информация. Селектор.
    """

    queryset = CharacterCompetency.objects.select_related(
        "character",
        "Competency",
        "inspector",
    )
    filter_class = CharacterCompetencyOrDetailFilter
