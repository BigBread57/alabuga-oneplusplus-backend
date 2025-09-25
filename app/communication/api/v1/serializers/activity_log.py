from rest_framework import serializers

from communication.models import ActivityLog


class ActivityLogListSerializer(serializers.ModelSerializer):
    """
    Журнал событий. Список.
    """

    class Meta:
        model = ActivityLog
        fields = (
            "id",
            "character",
            "text",
            "content_type",
            "object_id",
            "created_at",
            "updated_at",
        )
