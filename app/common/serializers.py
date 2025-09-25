from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ResponseDetailSerializer(serializers.Serializer):
    """Подробная информация в Response."""

    detail = serializers.CharField(
        label=_("Подробная информация о результате действия"),
        help_text=_("Подробная информация о результате действия"),
        required=True,
    )
