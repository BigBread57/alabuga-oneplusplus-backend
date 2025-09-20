from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Profile(AbstractBaseModel):
    """
    Профиль пользователя
    """

    avatar = models.ImageField(
        verbose_name=_('Аватар'),
        upload_to='avatars',
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        to=User,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="profile",
    )
    experience = models.IntegerField(
        verbose_name=_('Опыт'),
        default=0,
        help_text=_('Очки прогресса для повышения ранга'),
    )
    mana = models.IntegerField(
        verbose_name=_('Мана'),
        default=0,
        help_text=_('Игровая валюта для покупок'),
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.user
