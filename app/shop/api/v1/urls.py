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

user_purchase_urls = [
    path(
        route="user-purchases/list/",
        view=views.UserPurchaseListAPIView.as_view(),
        name="user-purchases-list",
    ),
    path(
        route="item/<int:pk>/detail/",
        view=views.UserPurchaseDetailAPIView.as_view(),
        name="user-purchases-detail",
    ),
    path(
        route="user-purchases/create/",
        view=views.UserPurchaseCreateAPIView.as_view(),
        name="user-purchases-create",
    ),
    path(
        route="user-purchases/<int:pk>/update-status/",
        view=views.UserPurchaseUpdateStatusAPIView.as_view(),
        name="user-purchases-update-status",
    ),
    path(
        route="user-purchases/<int:pk>/to-work/",
        view=views.UserPurchaseToWorkAPIView.as_view(),
        name="user-purchases-to-work",
    ),
]


urlpatterns = [
    *shop_item_category_urls,
    *shop_item_urls,
    *user_purchase_urls,
]
