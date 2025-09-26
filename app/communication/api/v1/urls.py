from django.urls import path

from communication.api.v1.views import (
    ActivityLogListAPIView,
    CommentCreateAPIView,
    PostListAPIView,
    TopicDetailAPIView,
    TopicListAPIView,
)
from communication.api.v1.views.activity_log import ActivityLogContentTypeListAPIView

app_name = "v1"

comment_urls = [
    path(
        route="comments/create/",
        view=CommentCreateAPIView.as_view(),
        name="comments-create",
    ),
]

post_urls = [
    path(
        route="posts/list/",
        view=PostListAPIView.as_view(),
        name="posts-list",
    ),
]

topic_urls = [
    path(
        route="topics/list/",
        view=TopicListAPIView.as_view(),
        name="topics-list",
    ),
    path(
        route="topics/<int:pk>/detail/",
        view=TopicDetailAPIView.as_view(),
        name="topics-detail",
    ),
]

activity_logs_urls = [
    path(
        route="activity-logs/list/",
        view=ActivityLogListAPIView.as_view(),
        name="activity-logs-list",
    ),
    path(
        route="activity-logs/content-types/list/",
        view=ActivityLogContentTypeListAPIView.as_view(),
        name="activity-logs-content-types-list",
    ),
]

urlpatterns = [
    *comment_urls,
    *post_urls,
    *topic_urls,
    *activity_logs_urls,
]
