from django.contrib import admin

from communication.models import ActivityLog, Comment, Post, Topic


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """
    Журнал действий.
    """

    list_display = (
        "id",
        "character",
        "text",
        "content_type",
    )
    list_filter = ("content_type",)
    search_fields = ("text",)
    ordering = ("-id",)
    autocomplete_fields = ("character",)
    list_select_related = ("character",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Комментарий.
    """

    list_display = (
        "id",
        "character",
        "text",
        "content_type",
    )
    list_filter = ("content_type",)
    search_fields = ("text",)
    ordering = ("-id",)
    autocomplete_fields = ("character",)
    list_select_related = ("character",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Пост.
    """

    list_display = (
        "id",
        "name",
        "character",
        "topic",
    )
    list_filter = ("topic",)
    search_fields = ("name", "text")
    ordering = ("-id",)
    autocomplete_fields = (
        "topic",
        "character",
    )
    list_select_related = (
        "topic",
        "character",
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    Тема.
    """

    list_display = (
        "id",
        "name",
    )
    list_filter = ("game_worlds",)
    search_fields = ("name",)
    ordering = ("-id",)
