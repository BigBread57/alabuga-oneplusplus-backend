from django.contrib import admin
from server.apps.alabuga_file.models import AlabugaFile
from server.apps.services.admin_mixin import AddCreatorForObjectMixin


@admin.register(AlabugaFile)
class AlabugaFileAdmin(AddCreatorForObjectMixin, admin.ModelAdmin[AlabugaFile]):
    """Админка для файлов."""

    list_display = (
        "id",
        "alabuga_file",
        "content_type",
        "object_id",
    )
    list_filter = ("content_type",)
    ordering = (
        "id",
        "alabuga_file",
        "content_type",
        "object_id",
    )
    readonly_fields = ("creator",)

    def save_model(self, request, obj, form, change) -> None:  # noqa: WPS110
        """Сохраняем информацию о том, кто создал объект через админку."""
        if not change:
            obj.creator = request.user
        return super().save_model(request, obj, form, change)  # type: ignore
