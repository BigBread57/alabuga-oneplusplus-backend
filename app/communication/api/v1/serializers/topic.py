from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from communication.api.v1.serializers.nested import PostNestedSerializer
from communication.models import Topic


class TopicListSerializer(serializers.ModelSerializer):
    """
    Тема. Список.
    """

    post_count = serializers.SerializerMethodField(
        label=_("Количество постов"),
        help_text=_("Количество постов"),
    )
    last_post = serializers.SerializerMethodField(
        label=_("Последний пост"),
        help_text=_("Последний пост"),
    )

    class Meta:
        model = Topic
        fields = (
            "id",
            "name",
            "shot_description",
            "description",
            "post_count",
            "last_post",
            "created_at",
            "updated_at",
        )

    def get_post_count(self, topic: Topic) -> int:
        """
        Количество постов в теме.
        """
        return topic.posts.count()

    def get_last_post(self, topic: Topic) -> ReturnDict | None:
        """
        Информация о последнем сообщении.
        """
        post = topic.posts.first()
        if post:
            return PostNestedSerializer(
                instance=topic.posts.first(),
                context=self.context,
            ).data
        return None


class TopicDetailSerializer(serializers.ModelSerializer):
    """
    Тема. Детальная информация.
    """

    posts = PostNestedSerializer(
        label=_("Посты"),
        help_text=_("Посты"),
        many=True,
    )

    class Meta:
        model = Topic
        fields = (
            "id",
            "name",
            "shot_description",
            "description",
            "posts",
            "created_at",
            "updated_at",
        )
