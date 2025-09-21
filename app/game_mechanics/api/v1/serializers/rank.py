from rest_framework import serializers

from app.game_mechanics.models import Rank
from django.utils.translation import gettext_lazy as _


class RankListSerializer(serializers.ModelSerializer):
    """
    Ранг. Список.
    """

    class Meta:
        model = Rank
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "required_experience",
            "order",
        )


class RankDetailSerializer(serializers.ModelSerializer):
    """
    Ранг. Детальная информация.
    """

    class Meta:
        model = Rank
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "required_experience",
            "order",
        )


class RankCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Ранг. Создание.
    """

    class Meta:
        model = Rank
        fields = (
            "name",
            "description",
            "icon",
            "required_experience",
            "order",
        )
