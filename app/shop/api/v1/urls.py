from django.urls import path

from app.shop.api.v1.views.shop_item_category import (
    ShopItemCategoryListAPIView,
    ShopItemCategoryCreateAPIView,
    ShopItemCategoryUpdateAPIView,
)
from app.shop.api.v1.views.shop_item import (
    ShopItemListAPIView,
    ShopItemCreateAPIView,
    ShopItemUpdateAPIView,
)
from app.shop.api.v1.views.user_purchase import UserPurchaseListAPIView, UserPurchaseCreateAPIView, \
    UserPurchaseUpdateAPIView, UserPurchaseToWorkAPIView, UserPurchaseDetailAPIView

app_name = "v1"


shop_item_category_urls = [
    path(
        route="item-category/list/",
        view=ShopItemCategoryListAPIView.as_view(),
        name="item-category-list",
    ),
    path(
        route="item-category/create/",
        view=ShopItemCategoryCreateAPIView.as_view(),
        name="item-category-create",
    ),
    path(
        route="item-category/<int:pk>/update/",
        view=ShopItemCategoryUpdateAPIView.as_view(),
        name="item-category-update",
    ),
]
shop_item_urls = [
    path(
        route="item/list/",
        view=ShopItemListAPIView.as_view(),
        name="item-list",
    ),
    path(
        route="item/create/",
        view=ShopItemCreateAPIView.as_view(),
        name="item-create",
    ),
    path(
        route="item/<int:pk>/update/",
        view=ShopItemUpdateAPIView.as_view(),
        name="item-update",
    ),
]

user_purchase_urls = [
    path(
        route="user-purchase/list/",
        view=UserPurchaseListAPIView.as_view(),
        name="user-purchase-list",
    ),
    path(
        route="item/<int:pk>/detail/",
        view=UserPurchaseDetailAPIView.as_view(),
        name="user-purchase-detail",
    ),
    path(
        route="user-purchase/create/",
        view=UserPurchaseCreateAPIView.as_view(),
        name="user-purchase-create",
    ),
    path(
        route="item/<int:pk>/update/",
        view=UserPurchaseUpdateAPIView.as_view(),
        name="user-purchase-update",
    ),
    path(
        route="item/<int:pk>/to-work/",
        view=UserPurchaseToWorkAPIView.as_view(),
        name="user-purchase-to-work",
    ),
]


urlpatterns = [
    *shop_item_category_urls,
    *shop_item_urls,
    *user_purchase_urls,
]
