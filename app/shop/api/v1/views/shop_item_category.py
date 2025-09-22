from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.common.permissions import UserHRPermission
from app.common.serializers import ResponseDetailSerializer
from app.common.views import QuerySelectorMixin
from app.shop.api.v1.selectors import ShopItemCategoryListFilterSerializer, ShopItemCategoryListSelector
from app.shop.api.v1.serializers import (
    ShopItemCategoryCreateOrUpdateSerializer,
    ShopItemCategoryDetailSerializer,
    ShopItemCategoryListSerializer,
)
from app.shop.models import ShopItemCategory


class ShopItemCategoryListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Категория товара в магазине. Список.
    """

    selector = ShopItemCategoryListSelector()
    serializer_class = ShopItemCategoryListSerializer
    filter_params_serializer_class = ShopItemCategoryListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[ShopItemCategoryListFilterSerializer],
        responses={
            status.HTTP_200_OK: ShopItemCategoryListSerializer(many=True),
        },
        tags=["shop:shop_item_category"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class ShopItemCategoryCreateAPIView(GenericAPIView):
    """
    Категория товара в магазине. Создание.
    """

    serializer_class = ShopItemCategoryCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=ShopItemCategoryCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: ShopItemCategoryDetailSerializer,
        },
        tags=["shop:shop_item_category"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop_item_category = serializer.save()

        return Response(
            data=ShopItemCategoryDetailSerializer(
                instance=shop_item_category,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class ShopItemCategoryUpdateAPIView(GenericAPIView):
    """
    Категория товара в магазине. Изменение.
    """

    queryset = ShopItemCategory.objects.all()
    serializer_class = ShopItemCategoryCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=ShopItemCategoryCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: ShopItemCategoryDetailSerializer,
        },
        tags=["shop:shop_item_category"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        placement_metering_device = self.get_object()
        serializer = self.get_serializer(
            instance=placement_metering_device,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        shop_item_category = serializer.save()
        if getattr(shop_item_category, "_prefetched_objects_cache", None):
            shop_item_category._prefetched_objects_cache = {}

        return Response(
            data=ShopItemCategoryDetailSerializer(
                instance=placement_metering_device,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class ShopItemCategoryDeleteAPIView(GenericAPIView):
    """
    Категория товара в магазине. Удаление.
    """

    queryset = ShopItemCategory.objects.all()
    permission_classes = (UserHRPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["shop:shop_item_category"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        shop_item_category = self.get_object()
        shop_item_category.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
