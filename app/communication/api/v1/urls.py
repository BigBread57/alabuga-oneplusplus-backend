from django.urls import path

from communication.api.v1 import views

app_name = "v1"

comment_urls = [
    path(
        route="comments/list/",
        view=views.CommentListAPIView.as_view(),
        name="comments-list",
    ),
    path(
        route="comments/create/",
        view=views.CommentCreateAPIView.as_view(),
        name="comments-create",
    ),
    path(
        route="comments/<int:pk>/update/",
        view=views.CommentUpdateAPIView.as_view(),
        name="comments-update",
    ),
    path(
        route="comments/<int:pk>/delete/",
        view=views.CommentDeleteAPIView.as_view(),
        name="comments-delete",
    ),
]

post_urls = [
    path(
        route="posts/list/",
        view=views.PostListAPIView.as_view(),
        name="posts-list",
    ),
    path(
        route="posts/<int:pk>/detail/",
        view=views.PostDetailAPIView.as_view(),
        name="posts-detail",
    ),
    path(
        route="posts/create/",
        view=views.PostCreateAPIView.as_view(),
        name="posts-create",
    ),
    path(
        route="posts/<int:pk>/update/",
        view=views.PostUpdateAPIView.as_view(),
        name="posts-update",
    ),
    path(
        route="posts/<int:pk>/delete/",
        view=views.PostDeleteAPIView.as_view(),
        name="posts-delete",
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
    path(
        route="topics/create/",
        view=views.TopicCreateAPIView.as_view(),
        name="topics-create",
    ),
    path(
        route="topics/<int:pk>/update/",
        view=views.TopicUpdateAPIView.as_view(),
        name="topics-update",
    ),
    path(
        route="topics/<int:pk>/delete/",
        view=views.TopicDeleteAPIView.as_view(),
        name="topics-delete",
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
    path(
        route="activity-logs/<int:pk>/read/",
        view=views.ActivityLogReadAPIView.as_view(),
        name="activity-logs-read",
    ),
    path(
        route="activity-logs/read-all/",
        view=views.ActivityLogReadAllAPIView.as_view(),
        name="activity-logs-read-all",
    ),
]

urlpatterns = [
    *comment_urls,
    *post_urls,
    *topic_urls,
    *activity_logs_urls,
]
