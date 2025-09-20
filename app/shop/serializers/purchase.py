from rest_framework import serializers

from apps.shop.models import UserPurchase


class UserPurchaseSerializer(serializers.ModelSerializer):
    """
    Покупка пользователя.
    """
    
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_category = serializers.CharField(source='item.category', read_only=True)
    processed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPurchase
        fields = (
            "id",
            "item",
            "item_name",
            "item_category",
            "price",
            "status",
            "delivery_info",
            "processed_by_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "price",
            "processed_by",
        )
        
    def get_processed_by_name(self, obj):
        """Получить имя обработчика."""
        if obj.processed_by:
            return obj.processed_by.get_full_name() or obj.processed_by.username
        return None
        

class PurchaseProcessSerializer(serializers.ModelSerializer):
    """
    Сериализатор обработки покупки (для HR).
    """
    
    class Meta:
        model = UserPurchase
        fields = (
            "status",
            "delivery_info",
        )
        
    def validate_status(self, value):
        """Проверка статуса."""
        allowed_statuses = [
            UserPurchase.Status.CONFIRMED,
            UserPurchase.Status.DELIVERED,
            UserPurchase.Status.CANCELLED,
        ]
        if value not in allowed_statuses:
            raise serializers.ValidationError("Недопустимый статус")
        return value