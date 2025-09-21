from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.common.permissions import UserHRPermission
from app.common.views import QuerySelectorMixin
from app.shop.api.v1.selectors import ShopItemListSelector, ShopItemListFilterSerializer, ShopItemDetailSelector
from app.shop.api.v1.serializers import (
    ShopItemListSerializer,
    ShopItemCreateOrUpdateSerializer,
    ShopItemDetailSerializer,
)
from app.shop.models import ShopItem


class ShopItemListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Товар в магазине. Список.
    """

    selector = ShopItemListSelector()
    serializer_class = ShopItemListSerializer
    filter_params_serializer_class = ShopItemListFilterSerializer
    search_fields = ("name", "category__name")

    @extend_schema(
        parameters=[ShopItemListFilterSerializer],
        responses={
            status.HTTP_200_OK: ShopItemListSerializer(many=True),
        },
        tags=["shop:shop_item"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)



class ShopItemDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Товар в магазине. Детальная информация.
    """

    selector = ShopItemDetailSelector()
    serializer_class = ShopItemDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: ShopItemDetailSerializer,
        },
        tags=["shop:shop_item"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """Детальная информация об объекте."""
        shop_item = self.get_object()
        serializer = self.get_serializer(instance=shop_item)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class ShopItemCreateAPIView(GenericAPIView):
    """
    Товар в магазине. Создание.
    """

    serializer_class = ShopItemCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=ShopItemCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: ShopItemDetailSerializer,
        },
        tags=["shop:shop_item"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop_item = serializer.save()

        return Response(
            data=ShopItemDetailSerializer(
                instance=shop_item,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class ShopItemUpdateAPIView(GenericAPIView):
    """
    Товар в магазине. Изменение.
    """

    queryset = ShopItem.objects.all()
    serializer_class = ShopItemCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=ShopItemCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: ShopItemDetailSerializer,
        },
        tags=["shop:shop_item"],
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
        shop_item = serializer.save()
        if getattr(shop_item, "_prefetched_objects_cache", None):
            shop_item._prefetched_objects_cache = {}

        return Response(
            data=ShopItemDetailSerializer(
                instance=placement_metering_device,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )
