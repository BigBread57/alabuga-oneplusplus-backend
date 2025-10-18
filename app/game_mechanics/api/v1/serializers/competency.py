from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.api.v1.serializers.nested import CompetencyNestedSerializer
from game_mechanics.models import Competency


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


class CompetencyListMaxLevelSerializer(serializers.ModelSerializer):
    """
    Компетенция. Список. Максимальный уровень.
    """

    class Meta:
        model = Competency
        fields = (
            "id",
            "name",
            "description",
            "level",
            "required_experience",
            "icon",
            "color",
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
