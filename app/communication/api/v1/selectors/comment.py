import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from communication.models import Comment


class CommentListFilterSerializer(serializers.Serializer):
    """
    Комментарий. Список. Сериализатор для фильтра.
    """

    text = serializers.CharField(
        label=_("Текст"),
        help_text=_("Текст"),
        required=False,
    )


class CommentListFilter(django_filters.FilterSet):
    """
    Комментарий. Список. Фильтр.
    """

    class Meta:
        model = Comment
        fields = ("text",)


class CommentListSelector(BaseSelector):
    """
    Комментарий. Список. Селектор.
    """

    queryset = Comment.objects.select_related(
        "character",
        "content_type",
    )
    filter_class = CommentListFilter


class CommentDetailSelector(BaseSelector):
    """
    Комментарий. Детальная информация. Селектор.
    """

    queryset = Comment.objects.select_related(
        "character",
        "content_type",
    )
