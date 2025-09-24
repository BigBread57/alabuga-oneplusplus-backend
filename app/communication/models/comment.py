from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Comment(AbstractBaseModel):
    """Комментарий."""

    user = models.ForeignKey(
        to="user.User",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="comments",
        db_index=True,
    )
    text = models.TextField(
        verbose_name=_("Текст"),
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
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")

    def __str__(self):
        return f"{self.user} - {self.content_type}"
