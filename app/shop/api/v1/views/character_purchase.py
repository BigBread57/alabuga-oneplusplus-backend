from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import (
    UserManagerPermission,
)
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from shop.api.v1.selectors import (
    CharacterPurchaseDetailSelector,
    CharacterPurchaseListFilterSerializer,
    CharacterPurchaseListSelector,
)
from shop.api.v1.serializers import (
    CharacterPurchaseCreateSerializer,
    CharacterPurchaseDetailSerializer,
    CharacterPurchaseListSerializer,
    CharacterPurchaseUpdateStatusSerializer,
)
from shop.api.v1.services import character_purchase_service
from shop.models import CharacterPurchase


class CharacterPurchaseListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Покупки пользователя. Список.
    """

    selector = CharacterPurchaseListSelector
    serializer_class = CharacterPurchaseListSerializer
    filter_params_serializer_class = CharacterPurchaseListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[CharacterPurchaseListFilterSerializer],
        responses={
            status.HTTP_200_OK: CharacterPurchaseListSerializer(many=True),
        },
        tags=["shop:character_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class CharacterPurchaseDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Покупки пользователя. Детальная информация.
    """

    selector = CharacterPurchaseDetailSelector
    serializer_class = CharacterPurchaseDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterPurchaseDetailSerializer,
        },
        tags=["shop:character_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        character_purchase = self.get_object()
        serializer = self.get_serializer(instance=character_purchase)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class CharacterPurchaseCreateAPIView(GenericAPIView):
    """
    Покупки пользователя. Создание.
    """

    serializer_class = CharacterPurchaseCreateSerializer

    @extend_schema(
        request=CharacterPurchaseCreateSerializer,
        responses={
            status.HTTP_201_CREATED: CharacterPurchaseDetailSerializer,
        },
        tags=["shop:character_purchase"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        character_purchase = character_purchase_service.create(
            validated_data=serializer.validated_data,
            buyer=request.user.active_character,
        )

        return Response(
            data=CharacterPurchaseDetailSerializer(
                instance=character_purchase,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class CharacterPurchaseUpdateStatusAPIView(GenericAPIView):
    """
    Покупки пользователя. Изменение.
    """

    queryset = CharacterPurchase.objects.all()
    serializer_class = CharacterPurchaseUpdateStatusSerializer

    @extend_schema(
        request=CharacterPurchaseUpdateStatusSerializer,
        responses={
            status.HTTP_200_OK: CharacterPurchaseDetailSerializer,
        },
        tags=["shop:character_purchase"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        character_purchase = self.get_object()
        serializer = self.get_serializer(
            instance=character_purchase,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        character_purchase = character_purchase_service.update(
            character_purchase=character_purchase,
            validated_data=serializer.validated_data,
        )

        if getattr(character_purchase, "_prefetched_objects_cache", None):
            character_purchase._prefetched_objects_cache = {}

        return Response(
            data=CharacterPurchaseDetailSerializer(
                instance=character_purchase,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class CharacterPurchaseToWorkAPIView(GenericAPIView):
    """
    Покупки пользователя. Взять в работу.
    """

    queryset = CharacterPurchase.objects.all()
    permission_classes = (UserManagerPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["shop:character_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Взять в работу.
        """
        character_purchase = self.get_object()
        character_purchase_service.to_work(
            character_purchase=character_purchase,
            manager=request.user,
        )
        return Response(
            data=ResponseDetailSerializer({"detail": _("Взято в работу")}).data,
            status=status.HTTP_200_OK,
        )
