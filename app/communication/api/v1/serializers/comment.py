from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from communication.models import Comment
from user.api.v1.serializers.nested import CharacterNestedSerializer


class CommentListSerializer(serializers.ModelSerializer):
    """
    Комментарий. Список.
    """

    character = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "uuid",
            "text",
            "character",
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    Комментарий. Детальная информация.
    """

    character = CharacterNestedSerializer(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "uuid",
            "text",
            "character",
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        )


class CommentCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Комментарий. Создание и обновление.
    """

    class Meta:
        model = Comment
        fields = (
            "text",
            "content_type",
            "object_id",
        )
