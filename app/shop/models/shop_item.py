from django.db import models
from django.utils.translation import gettext_lazy as _

from app.common.models import AbstractBaseModel


class ShopItem(AbstractBaseModel):
    """
    Товар в магазине.
    """

    name = models.CharField(
        verbose_name=_("Название"),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_("Описание"),
    )
    price = models.PositiveIntegerField(
        verbose_name=_("Цена в валюте"),
    )
    number = models.PositiveIntegerField(
        verbose_name=_("Количество"),
        help_text=_("Доступное количество товара. 0 - бесконечное количество"),
    )
    image = models.ImageField(
        verbose_name=_("Изображение"),
        upload_to="shop_items",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name=_("Активен"),
        default=True,
    )
    start_datetime = models.DateTimeField(
        verbose_name=_("Дата и время старта продаж"),
        null=True,
        blank=True,
    )
    time_to_buy = models.PositiveIntegerField(
        verbose_name=_("Время на покупку, в днях"),
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        to="shop.ShopItemCategory",
        verbose_name=_("Категория"),
        on_delete=models.CASCADE,
        related_name="shop_items",
    )
    parent = models.ForeignKey(
        to="self",
        verbose_name=_("Родительский товар"),
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
        help_text=_("Заполняется только при наличии rank и/или competency"),
    )
    rank = models.ForeignKey(
        to="experience.Rank",
        verbose_name=_("Ранг"),
        on_delete=models.SET_NULL,
        related_name="shop_items",
        blank=True,
        null=True,
    )
    competency = models.ForeignKey(
        to="experience.Competency",
        verbose_name=_("Компетенция"),
        on_delete=models.SET_NULL,
        related_name="shop_items",
        blank=True,
        null=True,
    )

    class Meta(AbstractBaseModel.Meta):
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.name
