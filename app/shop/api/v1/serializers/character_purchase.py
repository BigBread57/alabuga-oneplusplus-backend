from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from shop.api.v1.serializers.nested import ShopItemNestedSerializer
from shop.models import CharacterPurchase, ShopItem


class CharacterPurchaseListSerializer(serializers.ModelSerializer):
    """
    Покупки пользователя. Список.
    """

    shop_item = ShopItemNestedSerializer(
        label=_("Товар"),
        help_text=_("Товар"),
    )

    class Meta:
        model = CharacterPurchase
        fields = (
            "id",
            "price",
            "number",
            "discount",
            "total_sum",
            "status",
            "additional_info",
            "buyer",
            "shop_item",
        )


class CharacterPurchaseDetailSerializer(serializers.ModelSerializer):
    """
    Покупки пользователя. Детальная информация.
    """

    shop_item = ShopItemNestedSerializer(
        label=_("Товар"),
        help_text=_("Товар"),
        many=True,
    )
    status_display_name = serializers.SerializerMethodField(
        label=_("Название статуса"),
        help_text=_("Название статуса"),
    )
    next_statuses = serializers.SerializerMethodField(
        label=_("Доступные следующие статусы"),
        help_text=_("Доступные следующие статусы"),
    )

    class Meta:
        model = CharacterPurchase
        fields = (
            "id",
            "price",
            "number",
            "total_sum",
            "status",
            "status_display_name",
            "additional_info",
            "buyer",
            "shop_item",
            "next_statuses",
        )

    def get_status_display_name(self, character_purchase: CharacterPurchase) -> str:
        """
        Название статуса.
        """
        return character_purchase.get_status_display()

    def get_next_statuses(self, character_purchase: CharacterPurchase) -> list[str]:
        """
        Следующие доступные статусы.
        """
        match character_purchase.status:
            case CharacterPurchase.Statuses.PENDING:
                return [
                    CharacterPurchase.Statuses.CONFIRMED,
                    CharacterPurchase.Statuses.CANCELLED,
                ]
            case CharacterPurchase.Statuses.CONFIRMED:
                return [
                    CharacterPurchase.Statuses.DELIVERED,
                ]
            case _:
                return []


class CharacterPurchaseCreateSerializer(serializers.ModelSerializer):
    """
    Покупки пользователя. Создать.
    """

    shop_item = serializers.PrimaryKeyRelatedField(
        label=_("Товар в магазине"),
        help_text=_("Товар в магазине"),
        queryset=ShopItem.objects.select_related("category"),
        required=False,
    )

    class Meta:
        model = CharacterPurchase
        fields = (
            "id",
            "number",
            "shop_item",
        )

    def validate(self, attrs: dict[str, Any]):
        """
        Проверить количество.
        """
        shop_item = attrs["shop_item"]
        number = attrs["number"]
        if purchase_restriction := shop_item.purchase_restriction:
            if number > purchase_restriction:
                raise serializers.ValidationError(_(f"Вы не можете купить только {purchase_restriction} товаров"))

        return attrs


class CharacterPurchaseUpdateStatusSerializer(serializers.ModelSerializer):
    """
    Покупки пользователя. Изменить.
    """

    class Meta:
        model = CharacterPurchase
        fields = (
            "id",
            "additional_info",
            "status",
        )
