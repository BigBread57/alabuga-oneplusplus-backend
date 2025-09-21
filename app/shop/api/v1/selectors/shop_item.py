from rest_framework import serializers
from .models import ShopItem, ShopItemCategory


class ShopItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)
    rank_name = serializers.CharField(source='rank.name', read_only=True, allow_null=True)
    competency_name = serializers.CharField(source='competency.name', read_only=True, allow_null=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ShopItem
        fields = [
            'id',
            'name',
            'description',
            'category',
            'category_name',
            'price',
            'parent',
            'parent_name',
            'rank',
            'rank_name',
            'competency',
            'competency_name',
            'quantity',
            'image',
            'image_url',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None

    def validate(self, data):
        # Проверка, что либо parent, либо rank/competency заполнены
        parent = data.get('parent')
        rank = data.get('rank')
        competency = data.get('competency')

        if parent and (rank or competency):
            raise serializers.ValidationError(
                "Товар не может одновременно иметь родителя и ранг/компетенцию"
            )

        return data


class ShopItemListSerializer(ShopItemSerializer):
    class Meta:
        model = ShopItem
        fields = [
            'id',
            'name',
            'category_name',
            'price',
            'quantity',
            'image_url',
            'is_active',
            'created_at'
        ]