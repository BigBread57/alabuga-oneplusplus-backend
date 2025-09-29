from communication.api.v1.views.activity_log import (
    ActivityLogContentTypeListAPIView,
    ActivityLogListAPIView,
    ActivityLogReadAllAPIView,
    ActivityLogReadAPIView,
)
from communication.api.v1.views.comment import (
    CommentCreateAPIView,
    CommentDeleteAPIView,
    CommentListAPIView,
    CommentUpdateAPIView,
)
from communication.api.v1.views.post import (
    PostCreateAPIView,
    PostDeleteAPIView,
    PostDetailAPIView,
    PostListAPIView,
    PostUpdateAPIView,
)
from communication.api.v1.views.topic import (
    TopicCreateAPIView,
    TopicDeleteAPIView,
    TopicDetailAPIView,
    TopicListAPIView,
    TopicUpdateAPIView,
)

__all__ = (
    # Comment
    "CommentListAPIView",
    "CommentCreateAPIView",
    "CommentUpdateAPIView",
    "CommentDeleteAPIView",
    # Post
    "PostListAPIView",
    "PostDetailAPIView",
    "PostCreateAPIView",
    "PostUpdateAPIView",
    "PostDeleteAPIView",
    # Topic
    "TopicListAPIView",
    "TopicDetailAPIView",
    # ActivityLog
    "ActivityLogListAPIView",
    "ActivityLogContentTypeListAPIView",
    "ActivityLogReadAPIView",
    "ActivityLogReadAllAPIView",
    # Topic
    "TopicListAPIView",
    "TopicDetailAPIView",
    "TopicCreateAPIView",
    "TopicUpdateAPIView",
    "TopicDeleteAPIView",
)
