import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app.common.selectors import BaseSelector
from app.shop.models import ShopItemCategory


class ShopItemCategoryListFilterSerializer(serializers.Serializer):
    """
    Категория товара в магазине. Список. Сериализатор для фильтра.
    """

    name = serializers.CharField(
        label=_("Название категории"),
        help_text=_("Название категории"),
        required=False,
    )
    

class ShopItemCategoryListFilter(django_filters.FilterSet):
    """
    Категория товара в магазине. Список. Фильтр.
    """

    name = django_filters.CharFilter(
        label=_("Название прибора учета"),
        help_text=_("Название прибора учета"),
    )


    class Meta:
        model = ShopItemCategory
        fields = (
            "name",
        )


class ShopItemCategoryListSelector(BaseSelector):
    """
    Категория товара в магазине. Список. Селектор.
    """

    queryset = ShopItemCategory.objects.all()
    filter_class = ShopItemCategoryListFilter

