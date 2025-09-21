from rest_framework import serializers

from app.shop.models import ShopItemCategory, ShopItem


class ShopItemCategoryNestedSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Создание.
    """

    class Meta:
        model = ShopItemCategory
        fields = (
            "id",
            "name",
            "color",
        )



class ShopItemNestedSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Создание.
    """

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "price",
            "rank",
            "competency",
            "number",
            "image",
        )

