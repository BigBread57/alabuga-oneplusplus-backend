from django.contrib import admin
from django.utils.html import format_html

from .models import ShopItem, ShopItemCategory, UserPurchase


@admin.register(ShopItemCategory)
class ShopItemCategoryAdmin(admin.ModelAdmin):
    """
    Категория товара в магазине.
    """

    list_display = (
        "id",
        "name",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("name",)
    ordering = ("-id",)


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    """
    Товар в магазине.
    """

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "number",
        "rank",
        "competency",
        "is_active",
        "created_at",
        "image_preview",
    )
    list_filter = (
        "category",
        "is_active",
        "created_at",
        "rank",
        "competency",
    )
    search_fields = (
        "name",
        "description",
    )
    list_editable = (
        "price",
        "number",
        "is_active",
    )
    autocomplete_fields = (
        "parent",
        "category",
        "rank",
        "competency",
    )
    list_select_related = (
        "parent",
        "category",
        "rank",
        "competency",
    )
    ordering = ("-id",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Превью"


@admin.register(UserPurchase)
class UserPurchaseAdmin(admin.ModelAdmin):
    """
    Покупки пользователя.
    """

    list_display = ("id", "buyer", "shop_item", "price", "number", "total_sum", "status_with_color", "manager")
    list_filter = (
        "status",
        "shop_item__category",
    )
    search_fields = (
        "buyer__email",
        "buyer__first_name",
        "buyer__last_name",
        "shop_item__name",
    )
    autocomplete_fields = (
        "buyer",
        "shop_item",
        "manager",
    )
    list_select_related = (
        "buyer",
        "shop_item",
        "manager",
    )

    def status_with_color(self, obj):
        status_colors = {"PENDING": "gray", "CONFIRMED": "blue", "DELIVERED": "green", "CANCELLED": "red"}

        color = status_colors.get(obj.status, "gray")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 12px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_with_color.short_description = "Статус"
