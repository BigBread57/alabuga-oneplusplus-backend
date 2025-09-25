from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from communication.api.v1.serializers import TopicDetailSerializer, TopicListSerializer
from communication.models import Topic


class TopicListAPIView(GenericAPIView):
    """
    Тема. Список.
    """

    queryset = Topic.objects.all()
    serializer_class = TopicListSerializer
    search_fields = ("name",)

    @extend_schema(
        responses={
            status.HTTP_200_OK: TopicListSerializer(many=True),
        },
        tags=["communication:topic"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class TopicDetailAPIView(GenericAPIView):
    """
    Тема. Детальная информация.
    """

    queryset = Topic.objects.all()
    serializer_class = TopicDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: TopicDetailSerializer,
        },
        tags=["communication:topic"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        topic = self.get_object()
        serializer = self.get_serializer(instance=topic)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
