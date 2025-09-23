import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from shop.models import ShopItem, ShopItemCategory


class ShopItemListFilterSerializer(serializers.Serializer):
    """
    Товар в магазине. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название"),
        help_text=_("Название"),
        required=False,
    )
    category = serializers.PrimaryKeyRelatedField(
        label=_("Категория"),
        help_text=_("Категория"),
        queryset=ShopItemCategory.objects.all(),
        required=False,
    )


class ShopItemListFilter(django_filters.FilterSet):
    """
    Товар в магазине. Список. Фильтр.
    """

    category = django_filters.ModelMultipleChoiceFilter(
        label=_("Название"),
        help_text=_("Название"),
        queryset=ShopItemCategory.objects.all(),
    )

    class Meta:
        model = ShopItem
        fields = (
            "name",
            "category",
        )


class ShopItemListSelector(BaseSelector):
    """
    Товар в магазине. Список. Селектор.
    """

    queryset = (
        ShopItem.objects.select_related(
            "category",
        )
        .filter(
            is_active=True,
            parent__isnull=True,
        )
        .annotate(
            purchase_restriction=models.F("category__purchase_restriction"),
        )
    )
    filter_class = ShopItemListFilter


class ShopItemDetailSelector(BaseSelector):
    """
    Товар в магазине. Детальная информация. Селектор.
    """

    queryset = (
        ShopItem.objects.select_related(
            "category",
            "parent",
            "rank",
            "competency",
        )
        .prefetch_related(
            "children",
        )
        .filter(
            is_active=True,
            parent__isnull=True,
        )
        .annotate(
            purchase_restriction=models.F("category__purchase_restriction"),
        )
    )
    filter_class = ShopItemListFilter
