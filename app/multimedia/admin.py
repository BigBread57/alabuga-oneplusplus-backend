from django.contrib import admin

from multimedia.models import Multimedia


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    """Админка для файлов."""

    list_display = (
        "id",
        "multimedia",
        "content_type",
        "object_id",
    )
    list_filter = ("content_type",)
    ordering = (
        "id",
        "multimedia",
        "content_type",
        "object_id",
    )
    readonly_fields = ("creator",)

    def save_model(self, request, obj, form, change) -> None:  # noqa: WPS110
        """Сохраняем информацию о том, кто создал объект через админку."""
        if not change:
            obj.creator = request.user
        return super().save_model(request, obj, form, change)  # type: ignore
