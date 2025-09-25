from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from shop.models import ShopItem, ShopItemCategory


class ShopItemCategoryNestedSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Вложенный сериалайзер.
    """

    class Meta:
        model = ShopItemCategory
        fields = (
            "id",
            "name",
            "icon",
            "color",
        )


class ShopItemNestedSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Вложенный сериалайзер.
    """

    category = ShopItemCategoryNestedSerializer(
        label=_("Категория"),
        help_text=_("Категория"),
    )

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "category",
            "price",
            "rank",
            "competency",
            "number",
            "image",
        )
