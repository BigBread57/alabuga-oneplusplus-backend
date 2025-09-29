from datetime import datetime, timedelta
from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from game_mechanics.api.v1.serializers.nested import (
    CompetencyNestedSerializer,
    RankNestedSerializer,
)
from shop.api.v1.serializers.nested import (
    ShopItemCategoryNestedSerializer,
    ShopItemNestedSerializer,
)
from shop.models import ShopItem


class ShopItemListSerializer(serializers.ModelSerializer):
    """
    Товар в магазине. Список.
    """

    category = ShopItemCategoryNestedSerializer(
        label=_("Категория"),
        help_text=_("Категория"),
    )
    end_datetime = serializers.SerializerMethodField(
        label=_("Дата и время окончания продаж"),
        help_text=_("Дата и время окончания продаж"),
    )
    children = ShopItemNestedSerializer(
        label=_("Другой вид товара"),
        help_text=_("Другой вид товара"),
        many=True,
    )

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "description",
            "category",
            "price",
            "number",
            "image",
            "is_active",
            "start_datetime",
            "end_datetime",
            "purchase_restriction",
            "children",
        )

    def get_end_datetime(self, shop_item: ShopItem) -> datetime | None:
        """
        Дата и время окончания продаж.
        """
        if shop_item.start_datetime and shop_item.time_to_buy:
            return shop_item.start_datetime + timedelta(hours=shop_item.time_to_buy)
        return None


class ShopItemListForBuySerializer(serializers.ModelSerializer):
    """
    Товар в магазине. Список для покупки.
    """

    category = ShopItemCategoryNestedSerializer(
        label=_("Категория"),
        help_text=_("Категория"),
    )
    end_datetime = serializers.SerializerMethodField(
        label=_("Дата и время окончания продаж"),
        help_text=_("Дата и время окончания продаж"),
    )
    children = ShopItemNestedSerializer(
        label=_("Другой вид товара"),
        help_text=_("Другой вид товара"),
        many=True,
    )
    shop_discount = serializers.IntegerField(
        label=_("Скидка"),
        help_text=_("Скидка"),
    )

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "description",
            "category",
            "price",
            "number",
            "image",
            "is_active",
            "start_datetime",
            "end_datetime",
            "purchase_restriction",
            "children",
            "shop_discount",
        )

    def get_end_datetime(self, shop_item: ShopItem) -> datetime | None:
        """
        Дата и время окончания продаж.
        """
        if shop_item.start_datetime and shop_item.time_to_buy:
            return shop_item.start_datetime + timedelta(hours=shop_item.time_to_buy)
        return None


class ShopItemDetailSerializer(serializers.ModelSerializer):
    """
    Товар в магазине. Детальная информация.
    """

    category = ShopItemCategoryNestedSerializer(
        label=_("Категория"),
        help_text=_("Категория"),
    )
    rank = RankNestedSerializer(
        label=_("Ранг"),
        help_text=_("Ранг"),
    )
    competency = CompetencyNestedSerializer(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
    )
    children = ShopItemNestedSerializer(
        label=_("Дочерние элементы"),
        help_text=_("Дочерние элементы"),
        many=True,
    )
    end_datetime = serializers.SerializerMethodField(
        label=_("Дата и время окончания продаж"),
        help_text=_("Дата и время окончания продаж"),
    )

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "description",
            "category",
            "price",
            "children",
            "rank",
            "competency",
            "number",
            "image",
            "is_active",
            "end_datetime",
            "purchase_restriction",
        )

    def get_end_datetime(self, shop_item: ShopItem) -> datetime | None:
        """
        Дата и время окончания продаж.
        """
        if shop_item.start_datetime and shop_item.time_to_buy:
            return shop_item.start_datetime + timedelta(hours=shop_item.time_to_buy)
        return None


class ShopItemDetailForBuySerializer(serializers.ModelSerializer):
    """
    Товар в магазине. Детальная информация для покупки.
    """

    category = ShopItemCategoryNestedSerializer(
        label=_("Категория"),
        help_text=_("Категория"),
    )
    rank = RankNestedSerializer(
        label=_("Ранг"),
        help_text=_("Ранг"),
    )
    competency = CompetencyNestedSerializer(
        label=_("Компетенция"),
        help_text=_("Компетенция"),
    )
    children = ShopItemNestedSerializer(
        label=_("Дочерние элементы"),
        help_text=_("Дочерние элементы"),
        many=True,
    )
    end_datetime = serializers.SerializerMethodField(
        label=_("Дата и время окончания продаж"),
        help_text=_("Дата и время окончания продаж"),
    )
    shop_discount = serializers.IntegerField(
        label=_("Скидка"),
        help_text=_("Скидка"),
    )

    class Meta:
        model = ShopItem
        fields = (
            "id",
            "name",
            "description",
            "category",
            "price",
            "children",
            "rank",
            "competency",
            "number",
            "image",
            "is_active",
            "end_datetime",
            "purchase_restriction",
            "shop_discount",
        )

    def get_end_datetime(self, shop_item: ShopItem) -> datetime | None:
        """
        Дата и время окончания продаж.
        """
        if shop_item.start_datetime and shop_item.time_to_buy:
            return shop_item.start_datetime + timedelta(hours=shop_item.time_to_buy)
        return None


class ShopItemCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Товар в магазине. Создание.
    """

    class Meta:
        model = ShopItem
        fields = (
            "name",
            "description",
            "category",
            "price",
            "parent",
            "rank",
            "competency",
            "number",
            "image",
            "is_active",
        )

    def validate(self, attrs: dict[str, Any]):
        parent = attrs.get("parent", None)
        rank = attrs.get("rank", None)
        competency = attrs.get("competency", None)
        if (rank or competency) and not parent:
            raise ValidationError(
                _("Вы можете установить ранг или компетенцию только при заполнении родительского предмета")
            )
        return attrs


class ShopItemBuySerializer(serializers.Serializer):
    """
    Товар в магазине. Покупка.
    """

    number = serializers.IntegerField(
        label=_("Количество вещей для покупки"),
        help_text=_("Количество вещей для покупки"),
    )
