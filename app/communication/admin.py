from django.contrib import admin

from communication.models import Comment, Post, Topic


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Комментарий."""

    list_display = (
        "id",
        "user",
        "text",
    )
    ordering = ("-id",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
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
class TopicAdmin(admin.ModelAdmin):
    """тема."""

    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    ordering = ("-id",)
