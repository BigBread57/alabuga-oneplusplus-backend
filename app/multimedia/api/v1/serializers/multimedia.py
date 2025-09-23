from app.multimedia.models import Multimedia
from server.apps.services.serializers import ModelSerializerWithPermission


class MultimediaSerializer(ModelSerializerWithPermission):
    """Сериалайзер файлов."""

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


class CreateMultimediaSerializer(ModelSerializerWithPermission):
    """Создание файлов."""

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
        validated_data.update(
            {
                "creator": self.context.get("request").user,
                "company": validated_data.get(
                    "content_type",
                )
                .model_class()
                .objects.get(
                    id=validated_data.get("object_id"),
                )
                .company,
            },
        )
        return super().create(validated_data)
