from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ContentTypeNestedSerializer
from common.views import QuerySelectorMixin
from communication.api.v1.selectors import ActivityLogListSelector, \
    ActivityLogListFilterSerializer, ActivityLogContentTypeListSelector
from communication.api.v1.serializers import ActivityLogListSerializer


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
