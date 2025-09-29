from communication.api.v1.serializers.activity_log import (
    ActivityLogListSerializer,
    ActivityLogReadSerializer,
)
from communication.api.v1.serializers.comment import (
    CommentCreateOrUpdateSerializer,
    CommentDetailSerializer,
    CommentListSerializer,
)
from communication.api.v1.serializers.post import (
    PostCreateOrUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
)
from communication.api.v1.serializers.topic import (
    TopicCreateOrUpdateSerializer,
    TopicDetailSerializer,
    TopicListSerializer,
)

__all__ = (
    # Comment
    "CommentListSerializer",
    "CommentDetailSerializer",
    "CommentCreateOrUpdateSerializer",
    # Post
    "PostListSerializer",
    "PostDetailSerializer",
    "PostCreateOrUpdateSerializer",
    # ActivityLog
    "ActivityLogListSerializer",
    "ActivityLogReadSerializer",
    # Topic
    "TopicListSerializer",
    "TopicListSerializer",
    "TopicDetailSerializer",
    "TopicCreateOrUpdateSerializer",
)
