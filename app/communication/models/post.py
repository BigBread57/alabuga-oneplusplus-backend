from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Post(AbstractBaseModel):
    """Пост."""

    name = models.TextField(
        verbose_name=_("Название"),
    )
    text = models.TextField(
        verbose_name=_("Текст"),
    )
    character = models.ForeignKey(
        to="user.Character",
        verbose_name=_("Персонаж"),
        on_delete=models.CASCADE,
        related_name="posts",
    )
    topic = models.ForeignKey(
        to="communication.Topic",
        on_delete=models.CASCADE,
        verbose_name=_("Тема"),
        related_name="posts",
        db_index=True,
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        verbose_name=_("Родительский пост"),
        related_name="children",
        null=True,
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")

    def __str__(self):
        return f"{self.user} - {self.topic}"
