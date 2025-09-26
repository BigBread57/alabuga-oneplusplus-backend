from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.models import Comment
from user.api.v1.serializers.nested import CharacterNestedSerializer


class CommentListOrDetailSerializer(serializers.ModelSerializer):
    """
    Комментарий. Детальная информация/список.
    """

    character = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "character",
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
