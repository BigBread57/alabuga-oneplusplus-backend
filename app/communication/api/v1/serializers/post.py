from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.api.v1.serializers.nested import TopicNestedSerializer
from communication.models import Post
from user.api.v1.serializers.nested import CharacterNestedSerializer


class PostListSerializer(serializers.ModelSerializer):
    """
    Пост. Список.
    """

    character = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
    )
    topic = TopicNestedSerializer(
        label=_("Тема"),
        help_text=_("Тема"),
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "image",
            "name",
            "text",
            "character",
            "topic",
            "created_at",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Пост. Детальная информация.
    """

    character = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
    )
    topic = TopicNestedSerializer(
        label=_("Тема"),
        help_text=_("Тема"),
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "image",
            "name",
            "text",
            "character",
            "topic",
            "created_at",
            "updated_at",
        )


class PostCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Пост. Создание и обновление.
    """

    class Meta:
        model = Post
        fields = (
            "image",
            "name",
            "text",
            "topic",
        )
