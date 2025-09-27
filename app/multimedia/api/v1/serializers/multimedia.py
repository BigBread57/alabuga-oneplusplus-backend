from rest_framework import serializers

from multimedia.models import Multimedia


class MultimediaDetailSerializer(serializers.ModelSerializer):
    """
    Мультимедиа. Детальная информация.
    """

    class Meta:
        model = Multimedia
        fields = (
            "id",
            "multimedia",
            "created_at",
            "updated_at",
            "content_type",
            "object_id",
        )


class MultimediaCreateSerializer(serializers.ModelSerializer):
    """
    Мультимедиа. Создание.
    """

    class Meta:
        model = Multimedia
        fields = (
            "id",
            "multimedia",
            "content_type",
            "object_id",
        )
