from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AbstractBaseModel


class ShopItemCategory(AbstractBaseModel):
    """
    Категория товара в магазине.
    """

    uuid = models.UUIDField(
        verbose_name=_("UUID"),
        help_text=_("UUID"),
        default=uuid4,
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("Название категории"),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("Описание категории"),
    )
    icon = models.ImageField(
        verbose_name=_("Иконка"),
        upload_to="shop_item_categories",
        null=True,
        blank=True,
    )
    color = models.CharField(
        verbose_name=_("Цвет"),
        max_length=256,
        blank=True,
    )
    purchase_restriction = models.PositiveIntegerField(
        verbose_name=_("Ограничение на покупку, количество"),
        null=True,
        blank=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Категория товара в магазине")
        verbose_name_plural = _("Категории товаров в магазине")

    def __str__(self):
        return self.name
