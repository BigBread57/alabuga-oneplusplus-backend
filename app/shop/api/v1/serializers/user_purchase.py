from rest_framework import serializers
from app.shop.api.v1.serializers.nested import ShopItemNestedSerializer
from app.shop.models import UserPurchase
from django.utils.translation import gettext_lazy as _


class UserPurchaseListSerializer(serializers.ModelSerializer):
    """
    Покупки пользователя. Список.
    """

    shop_item = ShopItemNestedSerializer(
        label=_("Товар"),
        help_text=_("Товар"),
    )

    class Meta:
        model = UserPurchase
        fields = (
            "id",
            "price",
            "number",
            "total_sum",
            "status",
            "additional_info",
            "buyer",
            "shop_item",
        )


class UserPurchaseDetailSerializer(serializers.ModelSerializer):
    """
    Покупки пользователя. Детальная информация.
    """

    shop_item = ShopItemNestedSerializer(
        label=_("Товар"),
        help_text=_("Товар"),
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
        model = UserPurchase
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

    def get_status_display_name(self, user_purchase: UserPurchase) -> str:
        """
        Название статуса.
        """
        return user_purchase.get_status_display()

    def get_next_statuses(self, user_purchase: UserPurchase) -> list[str]:
        """
        Следующие доступные статусы.
        """
        match user_purchase.status:
            case UserPurchase.Statuses.PENDING:
                return [
                    UserPurchase.Statuses.CONFIRMED,
                    UserPurchase.Statuses.CANCELLED,
                ]
            case UserPurchase.Statuses.CONFIRMED:
                return [
                    UserPurchase.Statuses.DELIVERED,
                ]
            case _:
                return []


class UserPurchaseCreateSerializer(serializers.ModelSerializer):
    """
    Покупки пользователя. Создать.
    """

    class Meta:
        model = UserPurchase
        fields = (
            "id",
            "price",
            "number",
            "shop_item",
        )


class UserPurchaseUpdateSerializer(serializers.ModelSerializer):
    """
    Покупки пользователя. Изменить.
    """

    class Meta:
        model = UserPurchase
        fields = (
            "id",
            "additional_info",
            "status",
        )
