from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ShopItem, UserPurchase


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    """Административная панель для товаров магазина."""
    
    list_display = ('name', 'category', 'price', 'quantity', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('category', 'price')
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'description', 'category'),
        }),
        (_('Цена и количество'), {
            'fields': ('price', 'quantity'),
        }),
        (_('Медиа'), {
            'fields': ('image',),
        }),
        (_('Настройки'), {
            'fields': ('is_active',),
        }),
    )


@admin.register(UserPurchase)
class UserPurchaseAdmin(admin.ModelAdmin):
    """Административная панель для покупок."""
    
    list_display = ('user', 'item', 'price', 'status', 'created_at', 'processed_by')
    list_filter = ('status', 'item__category', 'created_at')
    search_fields = ('user__username', 'item__name')
    ordering = ('-created_at',)
    readonly_fields = ('price', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('user', 'item', 'price', 'status'),
        }),
        (_('Обработка'), {
            'fields': ('processed_by', 'delivery_info'),
        }),
        (_('Временные отметки'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )
