from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import AbstractBaseModel


class ItemCategory(models.TextChoices):
    """
    Категории товаров.
    """
    MERCH = 'MERCH', _('Мерч')
    TICKET = 'TICKET', _('Билет')
    BONUS = 'BONUS', _('Бонус')
    OTHER = 'OTHER', _('Другое')


class ShopItem(AbstractBaseModel):
    """
    Товар в магазине.
    """
    
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=256,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
    )
    category = models.CharField(
        verbose_name=_('Категория'),
        max_length=20,
        choices=ItemCategory.choices,
        default=ItemCategory.OTHER,
    )
    price = models.IntegerField(
        verbose_name=_('Цена в мане'),
        default=0,
    )
    quantity = models.IntegerField(
        verbose_name=_('Количество'),
        default=0,
        help_text=_('Доступное количество товара. 0 - бесконечное количество'),
    )
    image = models.ImageField(
        verbose_name=_('Изображение'),
        upload_to='shop_items',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name=_('Активен'),
        default=True,
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')
        ordering = ['category', 'price']
        
    def __str__(self):
        return f'{self.name} ({self.price} маны)'


class UserPurchase(AbstractBaseModel):
    """
    Покупки пользователя.
    """
    
    class Status(models.TextChoices):
        """
        Статус покупки.
        """
        PENDING = 'PENDING', _('В обработке')
        CONFIRMED = 'CONFIRMED', _('Подтверждена')
        DELIVERED = 'DELIVERED', _('Доставлена')
        CANCELLED = 'CANCELLED', _('Отменена')
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    item = models.ForeignKey(
        ShopItem,
        verbose_name=_('Товар'),
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    price = models.IntegerField(
        verbose_name=_('Цена покупки'),
        help_text=_('Цена на момент покупки'),
    )
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    delivery_info = models.TextField(
        verbose_name=_('Информация о доставке'),
        blank=True,
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Обработал'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_purchases',
    )
    
    class Meta(AbstractBaseModel.Meta):
        verbose_name = _('Покупка')
        verbose_name_plural = _('Покупки')
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.user} - {self.item.name} ({self.get_status_display()})'
