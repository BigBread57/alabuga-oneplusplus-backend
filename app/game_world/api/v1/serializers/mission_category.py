from datetime import datetime, timedelta

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.game_world.models import MissionCategory


class MissionCategoryListSerializer(serializers.ModelSerializer):
    """
    Категория миссии. Список.
    """

    class Meta:
        model = MissionCategory
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "color",
        )


class MissionCategoryDetailSerializer(serializers.ModelSerializer):
    """
    Категория миссии. Детальная информация.
    """

    class Meta:
        model = MissionCategory
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "color",
        )


class MissionCategoryCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Категория миссии. Создание.
    """

    class Meta:
        model = MissionCategory
        fields = (
            "icon",
            "name",
            "description",
            "color",
        )
