import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from common.selectors import BaseSelector
from shop.models import ShopItem
from user.models import Character


class CharacterActualForUserFilterSerializer(serializers.Serializer):
    """
    Персонаж пользователя. Детальная информация. Сериализатор для фильтра.
    """

    user = serializers.HiddenField(
        label=_("Пользователь"),
        help_text=_("Пользователь"),
        default=CurrentUserDefault(),
    )


class UserPurchaseDetailFilter(django_filters.FilterSet):
    """
    Персонаж пользователя. Детальная информация. Фильтр.
    """

    class Meta:
        model = Character
        fields = ("user",)


class CharacterActualForUserSelector(BaseSelector):
    """
    Персонаж пользователя. Детальная информация. Селектор.
    """

    queryset = (
        ShopItem.objects.select_related(
            "user",
            "game_world",
            "rank",
        )
        .prefetch_related(
            "character_artifacts__artifacts",
            "character_competencies__competencies",
            "character_missions__missions",
            "character_events__events",
        )
        .filter(
            is_active=True,
        )
    )
    filter_class = UserPurchaseDetailFilter
