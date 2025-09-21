from django.urls import path

from app.shop.api.v1.views.shop_item_category import ShopItemCategoryListAPIView, ShopItemCategoryCreateAPIView, \
    ShopItemCategoryUpdateAPIView

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


urlpatterns = [
    *shop_item_category_urls,
]
