from rest_framework import serializers

from apps.shop.models import ShopItem


class ShopItemListSerializer(serializers.ModelSerializer):
    """
    Товар магазина. Список объектов.
    """

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "description",
            "category",
            "price",
            "quantity",
            "image",
            "is_active",
        )
        

class ShopItemDetailSerializer(serializers.ModelSerializer):
    """
    Товар магазина. Детальная информация.
    """
    
    purchases_count = serializers.SerializerMethodField()
    can_purchase = serializers.SerializerMethodField()

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "description",
            "category",
            "price",
            "quantity",
            "image",
            "is_active",
            "purchases_count",
            "can_purchase",
            "created_at",
            "updated_at",
        )
        
    def get_purchases_count(self, obj):
        """Получить количество покупок товара."""
        return obj.purchases.count()
    
    def get_can_purchase(self, obj):
        """Проверить, может ли пользователь купить товар."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            # Проверяем активность товара
            if not obj.is_active:
                return False
            # Проверяем наличие маны
            if user.mana < obj.price:
                return False
            # Проверяем количество товара
            if obj.quantity > 0:
                return True
            # Если количество = 0, значит бесконечный товар
            return obj.quantity == 0
        return False