import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import Artifact


class ArtifactListFilterSerializer(serializers.Serializer):
    """
    Artifact. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )
    modifier = serializers.ChoiceField(
        label=_("Модификатор"),
        help_text=_("Модификатор"),
        choices=Artifact.Modifiers.choices,
        required=False,
    )


class ArtifactListFilter(django_filters.FilterSet):
    """
    Artifact. Список. Фильтр.
    """

    class Meta:
        model = Artifact
        fields = (
            "name",
            "modifier",
        )


class ArtifactListSelector(BaseSelector):
    """
    Артефакт. Список. Селектор.
    """

    queryset = Artifact.objects.all()
    filter_class = ArtifactListFilter
