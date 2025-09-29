import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from communication.models import Topic


class TopicListFilterSerializer(serializers.Serializer):
    """
    Тема. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )


class TopicListFilter(django_filters.FilterSet):
    """
    Тема. Список. Фильтр.
    """

    class Meta:
        model = Topic
        fields = ("name",)


class TopicListSelector(BaseSelector):
    """
    Тема. Список. Селектор.
    """

    queryset = Topic.objects.annotate(
        post_count=models.Count("posts"),
    )
    filter_class = TopicListFilter


class TopicDetailSelector(BaseSelector):
    """
    Тема. Детальная информация. Селектор.
    """

    queryset = Topic.objects.prefetch_related("game_worlds")
