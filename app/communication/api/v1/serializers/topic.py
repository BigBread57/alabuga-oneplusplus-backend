from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.models import Topic


class TopicListSerializer(serializers.ModelSerializer):
    """
    Тема. Список.
    """

    post_count = serializers.IntegerField(
        label=_("Количество постов"),
        help_text=_("Количество постов"),
    )

    class Meta:
        model = Topic
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "post_count",
            "created_at",
        )


class TopicDetailSerializer(serializers.ModelSerializer):
    """
    Тема. Детальная информация.
    """

    class Meta:
        model = Topic
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
            "created_at",
        )


class TopicCreateSerializer(serializers.ModelSerializer):
    """
    Тема. Создание.
    """

    class Meta:
        model = Topic
        fields = (
            "name",
            "description",
            "icon",
            "color",
        )


class TopicUpdateSerializer(serializers.ModelSerializer):
    """
    Тема. Изменение.
    """

    class Meta:
        model = Topic
        fields = (
            "name",
            "description",
            "icon",
            "color",
        )
