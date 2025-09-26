from rest_framework import serializers

from common.serializers import ContentTypeNestedSerializer
from communication.models import ActivityLog
from django.utils.translation import gettext_lazy as _


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
            "content_type",
            "object_id",
            "created_at",
        )
