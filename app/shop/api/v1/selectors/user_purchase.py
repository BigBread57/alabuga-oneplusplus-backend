import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from app.common.selectors import BaseSelector
from app.shop.models import UserPurchase


class UserPurchaseListFilterSerializer(serializers.Serializer):
    """
    Покупки пользователя. Список. Сериализатор для фильтра.
    """

    status = serializers.ChoiceField(
        label=_("Статус покупки пользователя"),
        help_text=_("Статус покупки пользователя"),
        choices=UserPurchase.Statuses.choices,
        required=True,
    )
    buyer = serializers.HiddenField(
        label=_("Покупатель"),
        help_text=_("Покупатель"),
        default=CurrentUserDefault(),
    )


class UserPurchaseListDetailSerializer(serializers.Serializer):
    """
    Покупки пользователя. Детальная информация. Сериализатор для фильтра.
    """

    buyer = serializers.HiddenField(
        label=_("Покупатель"),
        help_text=_("Покупатель"),
        default=CurrentUserDefault(),
    )



class UserPurchaseListFilter(django_filters.FilterSet):
    """
    Покупки пользователя. Список. Фильтр.
    """

    class Meta:
        model = UserPurchase
        fields = ("status", "buyer")


class UserPurchaseDetailFilter(django_filters.FilterSet):
    """
    Покупки пользователя. Детальная информация. Фильтр.
    """

    class Meta:
        model = UserPurchase
        fields = ("buyer",)


class UserPurchaseListSelector(BaseSelector):
    """
    Покупки пользователя. Список. Селектор.
    """

    queryset = UserPurchase.objects.select_related(
        "shop_item",
    ).all()
    filter_class = UserPurchaseListFilter


class UserPurchaseDetailSelector(BaseSelector):
    """
    Покупки пользователя. Детальная информация. Селектор.
    """

    queryset = UserPurchase.objects.select_related(
        "shop_item",
        "buyer",
        "manager",
    ).all()
    filter_class = UserPurchaseDetailFilter
