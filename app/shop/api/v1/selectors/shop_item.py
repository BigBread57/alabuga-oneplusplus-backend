import django_filters
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector
from game_world.models import Artifact
from shop.models import ShopItem, ShopItemCategory
from user.models import CharacterArtifact


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
        .prefetch_related(
            "children",
        )
        .filter(
            is_active=True,
            parent__isnull=True,
        )
    )
    filter_class = ShopItemListFilter


class ShopItemListForBuySelector(BaseSelector):
    """
    Товар в магазине. Список для покупки. Селектор.
    """

    filter_class = ShopItemListFilter

    def get_queryset(self, **kwargs) -> QuerySet[ShopItem]:
        active_character = kwargs["request"].user.active_character
        return (
            ShopItem.objects.select_related(
                "category",
            )
            .prefetch_related(
                "children",
            )
            .filter(
                is_active=True,
                parent__isnull=True,
                rank__character_ranks__character=active_character,
                competency__character_competencies__character=active_character,
            )
            .annotate(
                shop_discount=models.Subquery(
                    CharacterArtifact.objects.filter(
                        character=active_character,
                        artifact__modifier=Artifact.Modifiers.SHOP_DISCOUNT,
                    )
                    .values(
                        "artifact",
                    )
                    .annotate(sum=models.Sum("artifact__modifier_value"))
                    .values("sum")[:1]
                ),
            )
        )


class ShopItemDetailForBuySelector(BaseSelector):
    """
    Товар в магазине. Детальная информация о покупке. Селектор.
    """

    def get_queryset(self, **kwargs) -> QuerySet[ShopItem]:
        active_character = kwargs["request"].active_character
        return (
            ShopItem.objects.select_related(
                "category",
            )
            .prefetch_related(
                "children",
            )
            .filter(
                is_active=True,
                parent__isnull=True,
                rank__character_ranks__character=active_character,
                competency__character_competencies__character=active_character,
            )
            .annotate(
                shop_discount=models.Subquery(
                    CharacterArtifact.objects.filter(
                        character=active_character,
                        artifact__modifier=Artifact.Modifiers.SHOP_DISCOUNT,
                    )
                    .values(
                        "artifact",
                    )
                    .annotate(sum=models.Sum("artifact__modifier_value"))
                    .values("sum")[:1]
                ),
            )
        )


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
    )
    filter_class = ShopItemListFilter
