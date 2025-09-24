from rest_framework import serializers
from app.communication.models import Comment
from user.api.v1.serializers.user import BaseUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов."""

    user = BaseUserSerializer(

    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "text",
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        )


class CreateCommentSerializer(serializers.ModelSerializer):
    """Сериалайзер создания отзывов."""

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "content_type",
            "object_id",
        )
