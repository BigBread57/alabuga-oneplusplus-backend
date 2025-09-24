from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Multimedia(AbstractBaseModel):
    """
    Файл.
    """

    multimedia = models.FileField(
        verbose_name=_("Файл"),
        upload_to="private-media",
    )
    creator = models.ForeignKey(
        to="user.User",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь - создатель объекта"),
        related_name="%(class)s_created_objects",  # noqa: WPS323
        blank=True,
        null=True,
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
