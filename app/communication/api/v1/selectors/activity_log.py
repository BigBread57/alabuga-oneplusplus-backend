import django_filters
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


class ActivityLogListFilter(django_filters.FilterSet):
    """
    Журнал событий. Список. Фильтр.
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
