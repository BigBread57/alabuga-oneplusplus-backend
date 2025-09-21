from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from app.common.views import QuerySelectorMixin
from app.shop.api.v1.selectors import ShopItemCategoryListSelector


class ShopItemCategoryListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Категория товара в магазине. Список.
    """

    selector = ShopItemCategoryListSelector()
    serializer_class = ShopItemCategoryListSerializer
    filter_params_serializer_class = ShopItemCategoryFilterSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[ShopItemCategoryFilterSerializer],
        responses={
            status.HTTP_200_OK: ShopItemCategoryListSerializer(many=True),
        },
        tags=["individual_metering_device:metering_device"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """Список объектов."""
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class ShopItemCategoryDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """Прибор учета. Детальная информация об объекте."""

    selector = ShopItemCategoryDetailSelector()
    serializer_class = ShopItemCategoryDetailSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ShopItemCategoryDetailSerializer,
        },
        tags=["individual_metering_device:metering_device"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """Детальная информация об объекте."""
        metering_device = self.get_object()
        serializer = self.get_serializer(instance=metering_device)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
