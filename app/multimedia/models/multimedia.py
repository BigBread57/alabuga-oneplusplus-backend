from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Multimedia(AbstractBaseModel):
    """
    Мультимедиа.
    """

    multimedia = models.FileField(
        verbose_name=_("Файл"),
        upload_to="multimedia",
    )
    character = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Персонаж"),
        on_delete=models.CASCADE,
        related_name="multimedia",
    )
    content_type = models.ForeignKey(
        to="contenttypes.ContentType",
        verbose_name=_("Тип содержимого"),
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("Id объекта"),
    )
    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_id",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Файл")
        verbose_name_plural = _("Файлы")

    def __str__(self):
        return f"{self.multimedia}"

    @property
    def multimedia_name(self):
        """Возвращает имя файла без пути."""
        if self.multimedia:
            return self.multimedia.name.split('/')[-1]  # Только имя файла
        return ""