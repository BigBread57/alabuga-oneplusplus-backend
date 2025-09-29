from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.serializers import ContentTypeNestedSerializer
from communication.models import ActivityLog


class ActivityLogListSerializer(serializers.ModelSerializer):
    """
    Журнал событий. Список.
    """

    content_type = ContentTypeNestedSerializer(
        label=_("Тип содержимого"),
        help_text=_("Тип содержимого"),
    )

    class Meta:
        model = ActivityLog
        fields = (
            "id",
            "character",
            "text",
            "is_read",
            "content_type",
            "object_id",
            "created_at",
        )


class ActivityLogReadSerializer(serializers.ModelSerializer):
    """
    Журнал событий. Изменение.
    """

    class Meta:
        model = ActivityLog
        fields = ("is_read",)
