from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.models import Competency


class CompetencyListSerializer(serializers.ModelSerializer):
    """
    Компетенция. Список.
    """

    modifier_display_name = serializers.SerializerMethodField(
        label=_("Название статуса"),
        help_text=_("Название статуса"),
    )

    class Meta:
        model = Competency
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "modifier",
            "modifier_display_name",
            "modifier_value",
        )

    def get_modifier_display_name(self, competency: Competency) -> str:
        """
        Название статуса.
        """
        return competency.get_modifier_display()


class CompetencyDetailSerializer(serializers.ModelSerializer):
    """
    Компетенция. Детальная информация.
    """

    modifier_display_name = serializers.SerializerMethodField(
        label=_("Название статуса"),
        help_text=_("Название статуса"),
    )

    class Meta:
        model = Competency
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "modifier",
            "modifier_display_name",
            "modifier_value",
        )

    def get_modifier_display_name(self, competency: Competency) -> str:
        """
        Название статуса.
        """
        return competency.get_modifier_display()


class CompetencyCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Компетенция. Создание.
    """

    class Meta:
        model = Competency
        fields = (
            "name",
            "description",
            "icon",
            "modifier",
            "modifier_value",
        )
