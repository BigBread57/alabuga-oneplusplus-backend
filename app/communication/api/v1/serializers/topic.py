from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.models import Topic
from game_world.api.v1.serializers.nested import GameWorldNestedSerializer


class TopicListSerializer(serializers.ModelSerializer):
    """
    Тема. Список.
    """

    number_post = serializers.IntegerField(
        label=_("Количество постов"),
        help_text=_("Количество постов"),
    )

    class Meta:
        model = Topic
        fields = (
            "id",
            "name",
            "icon",
            "color",
            "number_post",
            "created_at",
        )


class TopicDetailSerializer(serializers.ModelSerializer):
    """
    Тема. Детальная информация.
    """

    game_worlds = GameWorldNestedSerializer(
        label=_("Игровые миры"),
        help_text=_("Игровые миры"),
    )

    class Meta:
        model = Topic
        fields = (
            "id",
            "name",
            "icon",
            "color",
            "game_worlds",
            "created_at",
            "updated_at",
        )


class TopicCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Тема. Создание и обновление.
    """

    class Meta:
        model = Topic
        fields = (
            "name",
            "icon",
            "color",
            "game_worlds",
        )
