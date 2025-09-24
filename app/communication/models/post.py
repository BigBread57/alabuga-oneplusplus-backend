from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class Post(AbstractBaseModel):
    """Пост."""

    text = models.TextField(
        verbose_name=_("Текст"),
    )
    user = models.ForeignKey(
        to="user.User",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="posts",
        db_index=True,
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
        db_index=True,
        null=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")

    def __str__(self):
        return f"{self.user} - {self.topic}"
