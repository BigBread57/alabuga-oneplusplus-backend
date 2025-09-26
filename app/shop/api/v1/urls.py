from django.urls import path

from shop.api.v1.views import (
    ShopItemCategoryCreateAPIView,
    ShopItemCategoryDeleteAPIView,
    ShopItemCategoryListAPIView,
    ShopItemCategoryUpdateAPIView,
    ShopItemCreateAPIView,
    ShopItemDeleteAPIView,
    ShopItemDetailAPIView,
    ShopItemDetailForBuyAPIView,
    ShopItemListAPIView,
    ShopItemListForBuyAPIView,
    ShopItemUpdateAPIView,
    UserPurchaseCreateAPIView,
    UserPurchaseDetailAPIView,
    UserPurchaseListAPIView,
    UserPurchaseToWorkAPIView,
    UserPurchaseUpdateStatusAPIView,
)

app_name = "v1"


shop_item_category_urls = [
    path(
        route="item-categories/list/",
        view=ShopItemCategoryListAPIView.as_view(),
        name="item-categories-list",
    ),
    path(
        route="item-categories/create/",
        view=ShopItemCategoryCreateAPIView.as_view(),
        name="item-categories-create",
    ),
    path(
        route="item-categories/<int:pk>/update/",
        view=ShopItemCategoryUpdateAPIView.as_view(),
        name="item-categories-update",
    ),
    path(
        route="item-categories/<int:pk>/delete/",
        view=ShopItemCategoryDeleteAPIView.as_view(),
        name="item-categories-delete",
    ),
]

shop_item_urls = [
    path(
        route="items/list/",
        view=ShopItemListAPIView.as_view(),
        name="items-list",
    ),
    path(
        route="items/list-for-buy",
        view=ShopItemListForBuyAPIView.as_view(),
        name="items-list-for-buy",
    ),
    path(
        route="items/<int:pk>/detail",
        view=ShopItemDetailAPIView.as_view(),
        name="items-detail",
    ),
    path(
        route="items/<int:pk>/detail-for-buy",
        view=ShopItemDetailForBuyAPIView.as_view(),
        name="items-detail-for-buy",
    ),
    path(
        route="items/create/",
        view=ShopItemCreateAPIView.as_view(),
        name="items-create",
    ),
    path(
        route="items/<int:pk>/update/",
        view=ShopItemUpdateAPIView.as_view(),
        name="items-update",
    ),
    path(
        route="items/<int:pk>/delete/",
        view=ShopItemDeleteAPIView.as_view(),
        name="items-delete",
    ),
]

user_purchase_urls = [
    path(
        route="user-purchases/list/",
        view=UserPurchaseListAPIView.as_view(),
        name="user-purchases-list",
    ),
    path(
        route="item/<int:pk>/detail/",
        view=UserPurchaseDetailAPIView.as_view(),
        name="user-purchases-detail",
    ),
    path(
        route="user-purchases/create/",
        view=UserPurchaseCreateAPIView.as_view(),
        name="user-purchases-create",
    ),
    path(
        route="user-purchases/<int:pk>/update-status/",
        view=UserPurchaseUpdateStatusAPIView.as_view(),
        name="user-purchases-update-status",
    ),
    path(
        route="user-purchases/<int:pk>/to-work/",
        view=UserPurchaseToWorkAPIView.as_view(),
        name="user-purchases-to-work",
    ),
]


urlpatterns = [
    *shop_item_category_urls,
    *shop_item_urls,
    *user_purchase_urls,
]
