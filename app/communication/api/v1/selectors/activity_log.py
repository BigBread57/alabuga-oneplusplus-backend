import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import When
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, CurrentCharacterDefault
from communication.models import ActivityLog


class ActivityLogListFilterSerializer(serializers.Serializer):
    """
    Журнал событий. Список. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )
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


class ActivityLogListSelector(BaseSelector):
    """
    Журнал событий. Список. Селектор.
    """

    queryset = ActivityLog.objects.select_related(
        "character",
        "content_type",
    )
    filter_class = ActivityLogListFilter


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
