from django.urls import path

from communication.api.v1 import views

app_name = "v1"

comment_urls = [
    path(
        route="comments/create/",
        view=views.CommentCreateAPIView.as_view(),
        name="comments-create",
    ),
]

post_urls = [
    path(
        route="posts/list/",
        view=views.PostListAPIView.as_view(),
        name="posts-list",
    ),
]

topic_urls = [
    path(
        route="topics/list/",
        view=views.TopicListAPIView.as_view(),
        name="topics-list",
    ),
    path(
        route="topics/<int:pk>/detail/",
        view=views.TopicDetailAPIView.as_view(),
        name="topics-detail",
    ),
]

activity_logs_urls = [
    path(
        route="activity-logs/list/",
        view=views.ActivityLogListAPIView.as_view(),
        name="activity-logs-list",
    ),
    path(
        route="activity-logs/content-types/list/",
        view=views.ActivityLogContentTypeListAPIView.as_view(),
        name="activity-logs-content-types-list",
    ),
]

urlpatterns = [
    *comment_urls,
    *post_urls,
    *topic_urls,
    *activity_logs_urls,
]
