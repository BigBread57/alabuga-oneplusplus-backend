from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.common.permissions import UserHRPermission
from app.common.serializers import ResponseDetailSerializer
from app.common.views import QuerySelectorMixin
from app.mission.api.v1.selectors import MissionDetailSelector, MissionListFilterSerializer, MissionListSelector
from app.mission.api.v1.serializers import (
    MissionCreateOrUpdateSerializer,
    MissionDetailSerializer,
    MissionListSerializer,
)
from app.mission.models import Mission


class MissionListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Миссия. Список.
    """

    selector = MissionListSelector()
    serializer_class = MissionListSerializer
    filter_params_serializer_class = MissionListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[MissionListFilterSerializer],
        responses={
            status.HTTP_200_OK: MissionListSerializer(many=True),
        },
        tags=["mission:mission"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class MissionDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Миссия. Детальная информация.
    """

    selector = MissionDetailSelector()
    serializer_class = MissionDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: MissionDetailSerializer,
        },
        tags=["mission:user_purchase"],
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


class MissionCreateAPIView(GenericAPIView):
    """
    Миссия. Создание.
    """

    serializer_class = MissionCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=MissionCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: MissionDetailSerializer,
        },
        tags=["mission:mission"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mission = serializer.save()

        return Response(
            data=MissionDetailSerializer(
                instance=mission,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class MissionUpdateAPIView(GenericAPIView):
    """
    Миссия. Изменение.
    """

    queryset = Mission.objects.all()
    serializer_class = MissionCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=MissionCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: MissionDetailSerializer,
        },
        tags=["mission:mission"],
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
        mission = serializer.save()
        if getattr(mission, "_prefetched_objects_cache", None):
            mission._prefetched_objects_cache = {}

        return Response(
            data=MissionDetailSerializer(
                instance=placement_metering_device,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class MissionDeleteAPIView(GenericAPIView):
    """
    Миссия. Удаление.
    """

    queryset = Mission.objects.all()
    permission_classes = (UserHRPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["mission:mission"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        mission = self.get_object()
        mission.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
