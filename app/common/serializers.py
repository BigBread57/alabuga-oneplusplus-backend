from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ResponseDetailSerializer(serializers.Serializer):
    """Подробная информация в Response."""

    detail = serializers.CharField(
        label=_("Подробная информация о результате действия"),
        help_text=_("Подробная информация о результате действия"),
        required=True,
    )


class ContentTypeNestedSerializer(serializers.ModelSerializer):
    """
    Тип содержимого. Список.
    """

    name = serializers.CharField(
        label=_("Название типа содержимого"),
        help_text=_("Название типа содержимого"),
    )
    color = serializers.CharField(
        label=_("Цвет"),
        help_text=_("Цвет"),
        default="",
    )

    class Meta:
        model = ContentType
        fields = (
            "id",
            "name",
            "color",
        )
