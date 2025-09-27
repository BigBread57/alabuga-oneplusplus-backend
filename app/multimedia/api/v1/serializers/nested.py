from rest_framework import serializers

from multimedia.models import Multimedia


class MultimediaNestedSerializer(serializers.ModelSerializer):
    """
    Мультимедиа. Вложенный сериалазер.
    """

    class Meta:
        model = Multimedia
        fields = (
            "id",
            "multimedia",
            "created_at",
        )
