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

    def create(self, validated_data):
        """При сохранении файла пользователь берется из запроса.

        Компания берется из связанного объекта.
        """
        validated_data.update({"creator": self.context.get("request").user})
        return super().create(validated_data)
