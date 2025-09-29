from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ContentTypeNestedSerializer, ResponseDetailSerializer
from common.views import QuerySelectorMixin
from communication.api.v1.selectors import (
    ActivityLogContentTypeListSelector,
    ActivityLogListFilterSerializer,
    ActivityLogListSelector,
    ActivityLogReadSelector,
)
from communication.api.v1.serializers import (
    ActivityLogListSerializer,
    ActivityLogReadSerializer,
)
from communication.api.v1.services import activity_log_service


class ActivityLogListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Журнал действий. Список.
    """

    selector = ActivityLogListSelector
    serializer_class = ActivityLogListSerializer
    filter_params_serializer_class = ActivityLogListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[ActivityLogListFilterSerializer],
        responses={
            status.HTTP_200_OK: ActivityLogListSerializer(many=True),
        },
        tags=["communication:activity_log"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class ActivityLogContentTypeListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Журнал действий. Тип содержимого. Список.
    """

    selector = ActivityLogContentTypeListSelector
    serializer_class = ContentTypeNestedSerializer
    search_fields = ("name",)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ContentTypeNestedSerializer(many=True),
        },
        tags=["communication:activity_log"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class ActivityLogReadAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Журнал действий. Прочитать.
    """

    selector = ActivityLogReadSelector
    serializer_class = ActivityLogReadSerializer

    @extend_schema(
        request=ActivityLogReadSerializer,
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["communication:activity_log"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        activity_log = self.get_object()
        serializer = self.get_serializer(
            instance=activity_log,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        activity_log = serializer.save()
        if getattr(activity_log, "_prefetched_objects_cache", None):
            activity_log._prefetched_objects_cache = {}

        return Response(
            data=ResponseDetailSerializer({"detail": _("Запись прочитана")}).data,
            status=status.HTTP_200_OK,
        )


class ActivityLogReadAllAPIView(GenericAPIView):
    """
    Журнал действий. Прочитать все.
    """

    queryset = ActivityLogReadSelector
    serializer_class = ActivityLogReadSerializer

    @extend_schema(
        request=ActivityLogReadSerializer,
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["communication:activity_log"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        activity_log_service.read_all(character=request.user.active_character)

        return Response(
            data=ResponseDetailSerializer({"detail": _("Все записи прочитаны")}).data,
            status=status.HTTP_200_OK,
        )
