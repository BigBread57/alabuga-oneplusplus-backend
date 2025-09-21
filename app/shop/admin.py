from django.contrib import admin
from django.utils.html import format_html

from .models import ShopItem, ShopItemCategory


@admin.register(ShopItemCategory)
class ShopItemCategoryAdmin(admin.ModelAdmin):
    """
    Категория товара в магазине.
    """
    list_display = (
        "id", 'name', 'created_at',
    )
    list_filter = (
        'created_at',)
    search_fields = ('name',)
    ordering = ('-id',)


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    """
    Товар в магазине.
    """
    list_display = (
        "id",
        'name',
        'category',
        'price',
        'quantity',
        'rank',
        'competency',
        'is_active',
        'created_at',
        'image_preview'
    )
    list_filter = (
        'category', 'is_active', 'created_at', 'rank', 'competency',
    )
    search_fields = (
        'name', 'description',
    )
    list_editable = (
        'price', 'quantity', 'is_active',
                     )
    autocomplete_fields = (
        'parent', 'category', 'rank', 'competency',)
    list_select_related = (
        'parent', 'category', 'rank', 'competency',
    )
    ordering = ('-id',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Превью"
