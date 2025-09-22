from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.game_mechanics.api.v1.serializers.nested import CompetencyNestedSerializer, RankNestedSerializer
from app.game_mechanics.models import RequiredRankCompetency


class RequiredRankCompetencyListSerializer(serializers.ModelSerializer):
    """
    Требования к компетенциям для получения ранга. Список.
    """

    rank = RankNestedSerializer(
        label=_("Ранг"),
        help_text=_("Ранг"),
    )
    competency = CompetencyNestedSerializer(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
    )

    class Meta:
        model = RequiredRankCompetency
        fields = (
            "id",
            "rank",
            "competency",
            "required_level",
        )


class RequiredRankCompetencyDetailSerializer(serializers.ModelSerializer):
    """
    Требования к компетенциям для получения ранга. Детальная информация.
    """

    rank = RankNestedSerializer(
        label=_("Ранг"),
        help_text=_("Ранг"),
    )
    competency = CompetencyNestedSerializer(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
    )

    class Meta:
        model = RequiredRankCompetency
        fields = (
            "id",
            "rank",
            "competency",
            "required_level",
        )


class RequiredRankCompetencyCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Требования к компетенциям для получения ранга. Создание.
    """

    class Meta:
        model = RequiredRankCompetency
        fields = (
            "rank",
            "competency",
            "required_level",
        )
