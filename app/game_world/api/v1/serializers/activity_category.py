from rest_framework import serializers

from game_world.models import ActivityCategory


class ActivityCategoryListSerializer(serializers.ModelSerializer):
    """
    Категория миссии. Список.
    """

    class Meta:
        model = ActivityCategory
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "color",
        )


class ActivityCategoryDetailSerializer(serializers.ModelSerializer):
    """
    Категория миссии. Детальная информация.
    """

    class Meta:
        model = ActivityCategory
        fields = (
            "id",
            "icon",
            "name",
            "description",
            "color",
        )


class ActivityCategoryCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Категория миссии. Создание.
    """

    class Meta:
        model = ActivityCategory
        fields = (
            "icon",
            "name",
            "description",
            "color",
        )
