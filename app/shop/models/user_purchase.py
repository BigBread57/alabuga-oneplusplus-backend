from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class UserPurchase(AbstractBaseModel):
    """
    Покупки пользователя.
    """

    class Status(models.TextChoices):
        """
        Статус покупки.
        """

        PENDING = "PENDING", _("В обработке")
        CONFIRMED = "CONFIRMED", _("Подтверждена")
        DELIVERED = "DELIVERED", _("Доставлена")
        CANCELLED = "CANCELLED", _("Отменена")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Пользователь"),
        on_delete=models.CASCADE,
        related_name="purchases",
    )
    item = models.ForeignKey(
        ShopItem,
        verbose_name=_("Товар"),
        on_delete=models.CASCADE,
        related_name="purchases",
    )
    price = models.IntegerField(
        verbose_name=_("Цена покупки"),
        help_text=_("Цена на момент покупки"),
    )
    status = models.CharField(
        verbose_name=_("Статус"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    delivery_info = models.TextField(
        verbose_name=_("Информация о доставке"),
        blank=True,
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Обработал"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_purchases",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Покупка")
        verbose_name_plural = _("Покупки")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.item.name} ({self.get_status_display()})"
