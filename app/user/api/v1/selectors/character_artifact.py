import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, CurrentCharacterDefault
from user.models import CharacterArtifact


class CharacterArtifactListOrDetailFilterSerializer(serializers.Serializer):
    """
    Артефакт персонажа. Список. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class CharacterArtifactListOrDetailFilter(django_filters.FilterSet):
    """
    Артефакт персонажа. Список. Фильтр.
    """

    class Meta:
        model = CharacterArtifact
        fields = (
            "character",
        )

class CharacterArtifactListSelector(BaseSelector):
    """
    Артефакт персонажа. Список. Селектор.
    """

    queryset = CharacterArtifact.objects.select_related(
        "character",
        "artifact",
    )
    filter_class = CharacterArtifactListOrDetailFilter


class CharacterArtifactDetailSelector(BaseSelector):
    """
    Артефакт персонажа. Детальная информация. Селектор.
    """

    queryset = CharacterArtifact.objects.select_related(
        "character",
        "artifact",
    )
    filter_class = CharacterArtifactListOrDetailFilter
