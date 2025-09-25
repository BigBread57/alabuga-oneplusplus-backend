from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.models import Comment
from user.api.v1.serializers.nested import UserNestedSerializer


class CommentListOrDetailSerializer(serializers.ModelSerializer):
    """
    Комментарий. Детальная информация/список.
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
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Комментарий. Создание.
    """

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "content_type",
            "object_id",
        )
