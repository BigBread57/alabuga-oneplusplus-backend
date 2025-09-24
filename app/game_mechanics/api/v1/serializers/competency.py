from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.api.v1.serializers.nested import CompetencyNestedSerializer
from game_mechanics.models import Competency
from game_world.api.v1.serializers.nested import GameWorldNestedSerializer


class CompetencyListSerializer(serializers.ModelSerializer):
    """
    Компетенция. Список.
    """

    parent = CompetencyNestedSerializer(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
    )

    class Meta:
        model = Competency
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "parent",
        )


class CompetencyDetailSerializer(serializers.ModelSerializer):
    """
    Компетенция. Детальная информация.
    """

    class Meta:
        model = Competency
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "parent",
            "game_world",
        )


class CompetencyCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Компетенция. Создание/изменение.
    """

    class Meta:
        model = Competency
        fields = (
            "name",
            "description",
            "icon",
            "color",
            "parent",
            "game_world",
        )
