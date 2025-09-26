from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.models import Comment, Post, Topic
from user.api.v1.serializers.nested import UserNestedSerializer


class PostNestedSerializer(serializers.ModelSerializer):
    """
    Пост. Вложенный сериалайзер.
    """

    class Meta:
        model = Post
        fields = (
            "id",
            "character",
            "name",
            "created_at",
        )


class TopicNestedSerializer(serializers.ModelSerializer):
    """
    Тема. Вложенный сериалайзер.
    """

    class Meta:
        model = Topic
        fields = (
            "id",
            "name",
            "description",
            "color",
            "icon",
        )


class CommentNestedSerializer(serializers.ModelSerializer):
    """
    Комментарий. Вложенный сериалайзер.
    """

    user = UserNestedSerializer(
        label=_("Пользователь"),
        help_text=_("Пользователь"),
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "text",
        )
