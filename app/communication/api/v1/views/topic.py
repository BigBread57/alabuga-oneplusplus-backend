from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import CharacterContentManagerPermission
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from communication.api.v1.selectors import (
    TopicDetailSelector,
    TopicListFilterSerializer,
    TopicListSelector,
)
from communication.api.v1.serializers import (
    TopicCreateOrUpdateSerializer,
    TopicDetailSerializer,
    TopicListSerializer,
)
from communication.models import Topic


class TopicListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Тема. Список.
    """

    selector = TopicListSelector
    serializer_class = TopicListSerializer
    filter_params_serializer_class = TopicListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[TopicListFilterSerializer],
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


class TopicDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Тема. Детальная информация.
    """

    selector = TopicDetailSelector
    serializer_class = TopicDetailSerializer
    permission_classes = (CharacterContentManagerPermission,)

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


class TopicCreateAPIView(GenericAPIView):
    """
    Тема. Создание.
    """

    serializer_class = TopicCreateOrUpdateSerializer
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        request=TopicCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: TopicDetailSerializer,
        },
        tags=["communication:topic"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        topic = serializer.save()

        return Response(
            data=TopicDetailSerializer(
                instance=topic,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class TopicUpdateAPIView(GenericAPIView):
    """
    Тема. Изменение.
    """

    queryset = Topic.objects.all()
    serializer_class = TopicCreateOrUpdateSerializer
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        request=TopicCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: TopicDetailSerializer,
        },
        tags=["communication:topic"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        topic = self.get_object()
        serializer = self.get_serializer(
            instance=topic,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        topic = serializer.save()
        if getattr(topic, "_prefetched_objects_cache", None):
            topic._prefetched_objects_cache = {}

        return Response(
            data=TopicDetailSerializer(
                instance=topic,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class TopicDeleteAPIView(GenericAPIView):
    """
    Тема. Удаление объекта.
    """

    queryset = Topic.objects.all()
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=["communication:topic"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        topic = self.get_object()
        topic.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
