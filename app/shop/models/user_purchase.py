from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel

User = get_user_model()


class UserPurchase(AbstractBaseModel):
    """
    Покупки пользователя.
    """

    class Statuses(models.TextChoices):
        """
        Статус покупки.
        """

        PENDING = "PENDING", _("В обработке")
        CONFIRMED = "CONFIRMED", _("Подтверждена")
        DELIVERED = "DELIVERED", _("Доставлена")
        CANCELLED = "CANCELLED", _("Отменена")

    price = models.PositiveIntegerField(
        verbose_name=_("Цена на момент покупки в валюте"),
    )
    number = models.PositiveIntegerField(
        verbose_name=_("Количество"),
    )
    total_sum = models.PositiveIntegerField(
        verbose_name=_("Общая сумма"),
    )
    status = models.CharField(
        verbose_name=_("Статус"),
        max_length=20,
        choices=Statuses.choices,
        default=Statuses.PENDING,
    )
    additional_info = models.TextField(
        verbose_name=_("Дополнительная информация"),
        blank=True,
    )
    buyer = models.ForeignKey(
        to=User,
        verbose_name=_("Покупатель"),
        on_delete=models.CASCADE,
        related_name="buyer_purchases",
    )
    shop_item = models.ForeignKey(
        to="shop.ShopItem",
        verbose_name=_("Товар"),
        on_delete=models.CASCADE,
        related_name="purchases",
    )
    manager = models.ForeignKey(
        to=User,
        verbose_name=_("Менеджер"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="manager_purchases",
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Покупка пользователя")
        verbose_name_plural = _("Покупки пользователей")

    def __str__(self):
        return f"{self.buyer} - {self.shop_item.name} ({self.get_status_display()})"
