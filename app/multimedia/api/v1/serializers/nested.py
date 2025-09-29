from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from multimedia.models import Multimedia


class MultimediaNestedSerializer(serializers.ModelSerializer):
    """
    Мультимедиа. Вложенный сериалазер.
    """

    multimedia_name = serializers.CharField(
        label=_("Покупатель"),
        help_text=_("Покупатель"),
    )

    class Meta:
        model = Multimedia
        fields = (
            "id",
            "multimedia",
            "multimedia_name",
            "created_at",
        )
