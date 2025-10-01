from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_mechanics.api.v1.serializers.nested import CompetencyNestedSerializer
from user.models import CharacterCompetency


class CharacterCompetencyListSerializer(serializers.ModelSerializer):
    """
    Уровень компетенции персонажа. Список.
    """

    competency = CompetencyNestedSerializer(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
    )
    content_type_id = serializers.IntegerField(
        label=_("ID тип содержимого"),
        help_text=_("ID тип содержимого"),
    )

    class Meta:
        model = CharacterCompetency
        fields = (
            "id",
            "competency",
            "experience",
            "is_received",
            "content_type_id",
            "received_datetime",
        )


class CharacterCompetencyDetailSerializer(serializers.ModelSerializer):
    """
    Уровень компетенции персонажа. Детальная информация.
    """

    competency = CompetencyNestedSerializer(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
    )
    content_type_id = serializers.IntegerField(
        label=_("ID тип содержимого"),
        help_text=_("ID тип содержимого"),
    )

    class Meta:
        model = CharacterCompetency
        fields = (
            "id",
            "competency",
            "experience",
            "is_received",
            "content_type_id",
            "received_datetime",
        )
