from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import UserHRPermission
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from mission_category.api.v1.selectors import (
    MissionCategoryDetailSelector,
    MissionCategoryListFilterSerializer,
    MissionCategoryListSelector,
)
from mission_category.api.v1.serializers import (
    MissionCategoryCreateOrUpdateSerializer,
    MissionCategoryDetailSerializer,
    MissionCategoryListSerializer,
)
from mission_category.models import MissionCategory


class MissionCategoryListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Категория миссии. Список.
    """

    selector = MissionCategoryListSelector()
    serializer_class = MissionCategoryListSerializer
    filter_params_serializer_class = MissionCategoryListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[MissionCategoryListFilterSerializer],
        responses={
            status.HTTP_200_OK: MissionCategoryListSerializer(many=True),
        },
        tags=["mission_category:mission_category"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class MissionCategoryDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Категория миссии. Детальная информация.
    """

    selector = MissionCategoryDetailSelector()
    serializer_class = MissionCategoryDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: MissionCategoryDetailSerializer,
        },
        tags=["mission_category:user_purchase"],
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


class MissionCategoryCreateAPIView(GenericAPIView):
    """
    Категория миссии. Создание.
    """

    serializer_class = MissionCategoryCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=MissionCategoryCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: MissionCategoryDetailSerializer,
        },
        tags=["mission_category:mission_category"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mission_category = serializer.save()

        return Response(
            data=MissionCategoryDetailSerializer(
                instance=mission_category,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class MissionCategoryUpdateAPIView(GenericAPIView):
    """
    Категория миссии. Изменение.
    """

    queryset = MissionCategory.objects.all()
    serializer_class = MissionCategoryCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=MissionCategoryCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: MissionCategoryDetailSerializer,
        },
        tags=["mission_category:mission_category"],
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
        mission_category = serializer.save()
        if getattr(mission_category, "_prefetched_objects_cache", None):
            mission_category._prefetched_objects_cache = {}

        return Response(
            data=MissionCategoryDetailSerializer(
                instance=placement_metering_device,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class MissionCategoryDeleteAPIView(GenericAPIView):
    """
    Категория миссии. Удаление.
    """

    queryset = MissionCategory.objects.all()
    permission_classes = (UserHRPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["mission_category:mission_category"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        mission_category = self.get_object()
        mission_category.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
