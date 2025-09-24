from django.contrib import admin
from app.communication.models import Comment
from app.communication.models.post import Post
from app.communication.models.topic import Topic


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin[Comment]):
    """Комментарий."""

    list_display = (
        "id",
        "user",
        "text",
    )
    search_fields = ("name",)
    ordering = ("-id",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin[Post]):
    """Пост."""

    list_display = (
        "id",
        "user",
        "topic",
        "parent",
    )
    list_filter = ("topic",)
    search_fields = ("topic__name",)
    ordering = ("-id",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin[Topic]):
    """тема."""

    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    ordering = ("-id",)
