from app.communication.api.serializers import BaseTopicSerializer
from app.communication.models import Post
from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.api.serializers import BaseUserSerializer


class PostSerializer(ModelSerializerWithPermission):
    """Сериалайзер отзывов."""

    user = BaseUserSerializer()
    topic = BaseTopicSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "topic",
            "text",
            "parent",
            "created_at",
            "updated_at",
        )


class CreatePostSerializer(ModelSerializerWithPermission):
    """Сериалайзер создания отзывов."""

    class Meta:
        model = Post
        fields = (
            "id",
            "topic",
            "text",
            "parent",
        )
