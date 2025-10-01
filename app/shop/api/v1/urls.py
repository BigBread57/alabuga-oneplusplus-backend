from django.urls import path

from shop.api.v1 import views

app_name = "v1"


shop_item_category_urls = [
    path(
        route="item-categories/list/",
        view=views.ShopItemCategoryListAPIView.as_view(),
        name="item-categories-list",
    ),
    path(
        route="item-categories/create/",
        view=views.ShopItemCategoryCreateAPIView.as_view(),
        name="item-categories-create",
    ),
    path(
        route="item-categories/<int:pk>/update/",
        view=views.ShopItemCategoryUpdateAPIView.as_view(),
        name="item-categories-update",
    ),
    path(
        route="item-categories/<int:pk>/delete/",
        view=views.ShopItemCategoryDeleteAPIView.as_view(),
        name="item-categories-delete",
    ),
]

shop_item_urls = [
    path(
        route="items/list/",
        view=views.ShopItemListAPIView.as_view(),
        name="items-list",
    ),
    path(
        route="items/list-for-buy",
        view=views.ShopItemListForBuyAPIView.as_view(),
        name="items-list-for-buy",
    ),
    path(
        route="items/<int:pk>/detail",
        view=views.ShopItemDetailAPIView.as_view(),
        name="items-detail",
    ),
    path(
        route="items/<int:pk>/detail-for-buy",
        view=views.ShopItemDetailForBuyAPIView.as_view(),
        name="items-detail-for-buy",
    ),
    path(
        route="items/create/",
        view=views.ShopItemCreateAPIView.as_view(),
        name="items-create",
    ),
    path(
        route="items/<int:pk>/update/",
        view=views.ShopItemUpdateAPIView.as_view(),
        name="items-update",
    ),
    path(
        route="items/<int:pk>/delete/",
        view=views.ShopItemDeleteAPIView.as_view(),
        name="items-delete",
    ),
]

character_purchase_urls = [
    path(
        route="character-purchases/list/",
        view=views.CharacterPurchaseListAPIView.as_view(),
        name="character-purchases-list",
    ),
    path(
        route="character-purchases/<int:pk>/detail/",
        view=views.CharacterPurchaseDetailAPIView.as_view(),
        name="character-purchases-purchases-detail",
    ),
    path(
        route="character-purchases/create/",
        view=views.CharacterPurchaseCreateAPIView.as_view(),
        name="character-purchases-create",
    ),
    path(
        route="character-purchases/<int:pk>/update-status/",
        view=views.CharacterPurchaseUpdateStatusAPIView.as_view(),
        name="character-purchases-update-status",
    ),
    path(
        route="character-purchases/<int:pk>/to-work/",
        view=views.CharacterPurchaseToWorkAPIView.as_view(),
        name="character-purchases-to-work",
    ),
]


urlpatterns = [
    *shop_item_category_urls,
    *shop_item_urls,
    *character_purchase_urls,
]
