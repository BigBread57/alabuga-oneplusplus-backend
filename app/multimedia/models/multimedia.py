from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel

User = get_user_model()


class Multimedia(AbstractBaseModel):
    """
    Файл.
    """

    alabuga_file = models.FileField(
        verbose_name=_("Файл"),
        upload_to="private-media",
    )
    creator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь - создатель объекта"),
        related_name="%(class)s_created_objects",  # noqa: WPS323
        blank=True,
        null=True,
    )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Тип содержимого"),
        on_delete=models.CASCADE,
        db_index=True,
    )
    object_id = models.PositiveIntegerField(_("Id объекта"))
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Файл")
        verbose_name_plural = _("Файлы")
