import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, CurrentCharacterDefault
from communication.models import ActivityLog


class ActivityLogForCharacterFilterSerializer(serializers.Serializer):
    """
    Журнал событий. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class ActivityLogListFilterSerializer(ActivityLogForCharacterFilterSerializer):
    """
    Журнал событий. Список. Сериализатор для фильтра.
    """

    content_type = serializers.PrimaryKeyRelatedField(
        label=_("Тип содержимого"),
        help_text=_("Тип содержимого"),
        queryset=ContentType.objects.all(),
        required=False,
    )


class ActivityLogListFilter(django_filters.FilterSet):
    """
    Журнал событий. Список. Фильтр.
    """

    class Meta:
        model = ActivityLog
        fields = (
            "character",
            "content_type",
        )


class ActivityLogReadFilter(django_filters.FilterSet):
    """
    Журнал событий. Изменение. Фильтр.
    """

    class Meta:
        model = ActivityLog
        fields = ("character",)


class ActivityLogListSelector(BaseSelector):
    """
    Журнал событий. Список. Селектор.
    """

    queryset = ActivityLog.objects.select_related(
        "character",
        "content_type",
    )
    filter_class = ActivityLogListFilter


class ActivityLogReadSelector(BaseSelector):
    """
    Журнал событий. Изменение. Селектор.
    """

    queryset = ActivityLog.objects.select_related(
        "character",
        "content_type",
    )
    filter_class = ActivityLogForCharacterFilterSerializer


class ActivityLogContentTypeListSelector(BaseSelector):
    """
    Журнал событий. Тип содержимого. Список. Селектор.
    """

    filter_class = ActivityLogListFilter

    def get_queryset(self, **kwargs) -> models.QuerySet:
        active_character = self.request.user.active_character
        return ContentType.objects.filter(
            id__in=ActivityLog.objects.filter(
                character=active_character,
            )
            .values_list("content_type", flat=True)
            .distinct()
        )
