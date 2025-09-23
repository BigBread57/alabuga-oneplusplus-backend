from rest_framework import serializers

from game_mechanics.models import Competency, Rank


class RankNestedSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Вложенный сериалайзер.
    """

    class Meta:
        model = Rank
        fields = (
            "id",
            "name",
            "description",
            "order",
        )


class CompetencyNestedSerializer(serializers.ModelSerializer):
    """
    Компетенция. Вложенный сериалайзер.
    """

    class Meta:
        model = Competency
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
        )
