from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.api.v1.serializers.nested import TopicNestedSerializer
from communication.models import Post
from user.api.v1.serializers.nested import UserNestedSerializer


class PostListSerializer(serializers.ModelSerializer):
    """
    Пост.
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
            "user",
            "topic",
            "text",
            "parent",
            "created_at",
            "updated_at",
        )


class PostCreateSerializer(serializers.ModelSerializer):
    """
    Пост.
    """

    class Meta:
        model = Post
        fields = (
            "id",
            "topic",
            "text",
            "parent",
        )
