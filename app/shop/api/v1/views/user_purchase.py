from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import UserHRPermission, UserManagerForObjectPermission, UserManagerPermission
from common.views import QuerySelectorMixin
from shop.api.v1.selectors import (
    UserPurchaseDetailSelector,
    UserPurchaseListFilterSerializer,
    UserPurchaseListSelector,
)
from shop.api.v1.serializers import (
    UserPurchaseCreateSerializer,
    UserPurchaseDetailSerializer,
    UserPurchaseListSerializer,
    UserPurchaseUpdateSerializer,
)
from shop.api.v1.services import user_purchase_service
from shop.models import UserPurchase


class UserPurchaseListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Покупки пользователя. Список.
    """

    selector = UserPurchaseListSelector
    serializer_class = UserPurchaseListSerializer
    filter_params_serializer_class = UserPurchaseListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[UserPurchaseListFilterSerializer],
        responses={
            status.HTTP_200_OK: UserPurchaseListSerializer(many=True),
        },
        tags=["shop:user_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class UserPurchaseDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Покупки пользователя. Детальная информация.
    """

    selector = UserPurchaseDetailSelector
    serializer_class = UserPurchaseDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: UserPurchaseDetailSerializer,
        },
        tags=["shop:user_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        user_purchase = self.get_object()
        serializer = self.get_serializer(instance=user_purchase)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class UserPurchaseCreateAPIView(GenericAPIView):
    """
    Покупки пользователя. Создание.
    """

    serializer_class = UserPurchaseCreateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=UserPurchaseCreateSerializer,
        responses={
            status.HTTP_201_CREATED: UserPurchaseDetailSerializer,
        },
        tags=["shop:user_purchase"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_purchase = user_purchase_service.create(
            validated_data=serializer.validated_data,
            buyer=request.user,
        )

        return Response(
            data=UserPurchaseDetailSerializer(
                instance=user_purchase,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class UserPurchaseUpdateAPIView(GenericAPIView):
    """
    Покупки пользователя. Изменение.
    """

    queryset = UserPurchase.objects.all()
    serializer_class = UserPurchaseUpdateSerializer
    permission_classes = (UserManagerForObjectPermission,)

    @extend_schema(
        request=UserPurchaseUpdateSerializer,
        responses={
            status.HTTP_200_OK: UserPurchaseDetailSerializer,
        },
        tags=["shop:user_purchase"],
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
        user_purchase = user_purchase_service.update(
            validated_data=serializer.validated_data,
            buyer=request.user,
        )

        if getattr(user_purchase, "_prefetched_objects_cache", None):
            user_purchase._prefetched_objects_cache = {}

        return Response(
            data=UserPurchaseDetailSerializer(
                instance=placement_metering_device,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class UserPurchaseToWorkAPIView(GenericAPIView):
    """
    Покупки пользователя. Взять в работу.
    """

    queryset = UserPurchase.objects.all()
    serializer_class = UserPurchaseUpdateSerializer
    permission_classes = (UserManagerPermission,)

    @extend_schema(
        request=UserPurchaseUpdateSerializer,
        responses={
            status.HTTP_200_OK: UserPurchaseDetailSerializer,
        },
        tags=["shop:user_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Взять в работу.
        """
        user_purchase = self.get_object()
        user_purchase_service.to_work(
            user_purchase=user_purchase,
            manager=request.user,
        )
        return Response(status=status.HTTP_200_OK)
