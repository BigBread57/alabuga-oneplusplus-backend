import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from common.selectors import BaseSelector
from shop.models import CharacterPurchase, ShopItemCategory


class CharacterPurchaseListFilterSerializer(serializers.Serializer):
    """
    Покупки пользователя. Список. Сериализатор для фильтра.
    """

    status = serializers.ChoiceField(
        label=_("Статус покупки пользователя"),
        help_text=_("Статус покупки пользователя"),
        choices=CharacterPurchase.Statuses.choices,
        required=False,
    )
    shop_item_category = serializers.PrimaryKeyRelatedField(
        label=_("Категория товара"),
        help_text=_("Категория товара"),
        queryset=ShopItemCategory.objects.all(),
        required=False,
    )
    buyer = serializers.HiddenField(
        label=_("Покупатель"),
        help_text=_("Покупатель"),
        default=CurrentUserDefault(),
    )


class CharacterPurchaseListFilter(django_filters.FilterSet):
    """
    Покупки пользователя. Список. Фильтр.
    """

    shop_item_category = django_filters.ModelChoiceFilter(
        label=_("Категория товара"),
        help_text=_("Категория товара"),
        queryset=ShopItemCategory.objects.all(),
        field_name="shop_item__category",
    )

    class Meta:
        model = CharacterPurchase
        fields = ("status", "buyer", "shop_item__category")


class CharacterPurchaseListSelector(BaseSelector):
    """
    Покупки пользователя. Список. Селектор.
    """

    queryset = CharacterPurchase.objects.select_related(
        "shop_item__category",
    )
    filter_class = CharacterPurchaseListFilter


class CharacterPurchaseDetailSelector(BaseSelector):
    """
    Покупки пользователя. Детальная информация. Селектор.
    """

    queryset = CharacterPurchase.objects.select_related(
        "shop_item__category",
        "buyer",
        "manager",
    )
