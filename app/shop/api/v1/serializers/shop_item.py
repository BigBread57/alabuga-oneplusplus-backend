from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.shop.api.v1.serializers.nested import ShopItemCategoryNestedSerializer, ShopItemNestedSerializer
from app.shop.models import ShopItem
from django.utils.translation import gettext_lazy as _


class ShopItemListSerializer(serializers.ModelSerializer):
    """
    Товар в магазине. Список
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
            "description",
            "category",
            "price",
            "number",
            "image",
            "is_active",
        )


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
        )


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

    def validate(self, attrs):
        parent = attrs.get("parent", None)
        rank = attrs.get("rank", None)
        competency = attrs.get("competency", None)
        if (rank or competency) and not parent:
            raise ValidationError(
                _(
                    "Вы можете установить ранг или компетенцию только при заполнении родительского предмета"
                )
            )
        return attrs
