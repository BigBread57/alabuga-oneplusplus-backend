from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import AbstractBaseModel


class BoardingStep(AbstractBaseModel):
    """
    Шаг онбординга.
    """

    title = models.CharField(
        verbose_name=_("Заголовок"),
        max_length=256,
    )
    content = models.TextField(
        verbose_name=_("Контент"),
        help_text=_("Интересные факты о космосе и платформе"),
    )
    order = models.IntegerField(
        verbose_name=_("Порядок"),
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Активен"),
        default=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Шаг онбординга")
        verbose_name_plural = _("Шаги онбординга")
        ordering = ["order"]

    def __str__(self):
        return self.title


class UserBoardingProgress(AbstractBaseModel):
    """
    Прогресс пользователя в онбординге.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="boarding_progress",
    )
    step = models.ForeignKey(
        BoardingStep,
        verbose_name=_("Шаг"),
        on_delete=models.CASCADE,
        related_name="user_progress",
    )
    completed_at = models.DateTimeField(
        verbose_name=_("Завершен"),
        null=True,
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Прогресс онбординга")
        verbose_name_plural = _("Прогресс онбординга")
        unique_together = ["user", "step"]

    def __str__(self):
        return f"{self.user} - {self.step.title}"
