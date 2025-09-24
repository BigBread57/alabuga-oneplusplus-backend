from django.urls import path

from communication.api.v1.views import CommentCreateAPIView, PostListAPIView, TopicDetailAPIView, TopicListAPIView

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

urlpatterns = [
    *comment_urls,
    *post_urls,
    *topic_urls,
]
