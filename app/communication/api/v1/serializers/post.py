from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.api.v1.serializers.nested import PostNestedSerializer, TopicNestedSerializer
from communication.models import Post
from user.api.v1.serializers.nested import UserNestedSerializer


class PostListSerializer(serializers.ModelSerializer):
    """
    Пост. Список.
    """

    user = UserNestedSerializer(
        label=_("Пользователь"),
        help_text=_("Пользователь"),
    )
    topic = TopicNestedSerializer(
        label=_("Тема"),
        help_text=_("Тема"),
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "name",
            "text",
            "parent",
            "created_at",
            "updated_at",
            "user",
            "topic",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Пост. Детальная информация.
    """

    user = UserNestedSerializer(
        label=_("Пользователь"),
        help_text=_("Пользователь"),
    )
    parent = PostNestedSerializer(
        label=_("Родительский пост"),
        help_text=_("Родительский пост"),
    )
    topic = TopicNestedSerializer(
        label=_("Тема"),
        help_text=_("Тема"),
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "name",
            "text",
            "parent",
            "created_at",
            "updated_at",
            "user",
            "topic",
        )


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Пост. Создание.
    """

    class Meta:
        model = Post
        fields = (
            "name",
            "text",
            "topic",
            "parent",
        )


class PostUpdateSerializer(serializers.ModelSerializer):
    """
    Пост. Изменение.
    """

    class Meta:
        model = Post
        fields = (
            "name",
            "text",
            "topic",
            "parent",
        )
