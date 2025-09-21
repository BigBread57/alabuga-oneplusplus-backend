from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class UserArtifact(AbstractBaseModel):
    """
    Артефакты пользователя.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="artifacts",
    )
    artifact = models.ForeignKey(
        Artifact,
        verbose_name=_("Артефакт"),
        on_delete=models.CASCADE,
        related_name="owners",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Артефакт пользователя")
        verbose_name_plural = _("Артефакты пользователей")
        unique_together = ["user", "artifact"]

    def __str__(self):
        return f"{self.user} - {self.artifact.name}"
