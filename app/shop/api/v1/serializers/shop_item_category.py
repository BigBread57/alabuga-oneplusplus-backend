from rest_framework import serializers

from shop.models import ShopItemCategory


class ShopItemCategoryListSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Список.
    """

    class Meta:
        model = ShopItemCategory
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
        )


class ShopItemCategoryDetailSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Детальная информация.
    """

    class Meta:
        model = ShopItemCategory
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "color",
        )


class ShopItemCategoryCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Категория товара в магазине. Создание.
    """

    class Meta:
        model = ShopItemCategory
        fields = (
            "name",
            "description",
            "icon",
            "color",
        )
