from django.contrib import admin

from multimedia.models import Multimedia


@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    """
    Мультимедиа.
    """

    list_display = (
        "id",
        "multimedia",
        "content_type",
        "object_id",
    )
    list_filter = ("content_type",)
    ordering = (
        "-id",
    )
    readonly_fields = ("character",)

    def save_model(self, request, obj, form, change) -> None:  # noqa: WPS110
        """Сохраняем информацию о том, кто создал объект через админку."""
        if not change:
            obj.character = request.user.actual_character
        return super().save_model(request, obj, form, change)  # type: ignore
