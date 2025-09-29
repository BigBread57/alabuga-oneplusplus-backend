import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from communication.models import Post, Topic


class PostListFilterSerializer(serializers.Serializer):
    """
    Пост. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )
    topic = serializers.PrimaryKeyRelatedField(
        label=_("Тема"),
        help_text=_("Тема"),
        queryset=Topic.objects.all(),
        required=False,
    )


class PostListFilter(django_filters.FilterSet):
    """
    Пост. Список. Фильтр.
    """

    class Meta:
        model = Post
        fields = (
            "name",
            "topic",
        )


class PostListSelector(BaseSelector):
    """
    Пост. Список. Селектор.
    """

    queryset = Post.objects.select_related(
        "character",
        "topic",
    )
    filter_class = PostListFilter


class PostDetailSelector(BaseSelector):
    """
    Пост. Детальная информация. Селектор.
    """

    queryset = Post.objects.select_related(
        "character",
        "topic",
    )
