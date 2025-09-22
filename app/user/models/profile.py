from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel

User = get_user_model()


class Profile(AbstractBaseModel):
    """
    Профиль пользователя
    """

    avatar = models.ImageField(
        verbose_name=_("Аватар"),
        upload_to="avatars",
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        to=User,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="profile",
    )
    currency = models.IntegerField(
        verbose_name=_("Валюта"),
        default=0,
        help_text=_("Игровая валюта для покупок"),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.user
