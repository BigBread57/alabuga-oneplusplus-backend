from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_world.api.v1.selectors import (
    EventArtifactDetailSelector,
    EventArtifactListFilterSerializer,
    EventArtifactListSelector,
)
from game_world.api.v1.serializers import (
    EventArtifactCreateOrUpdateSerializer,
    EventArtifactDetailSerializer,
    EventArtifactListSerializer,
)
from game_world.models import EventArtifact


class EventArtifactListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Артефакты за выполнение события. Список.
    """

    selector = EventArtifactListSelector
    serializer_class = EventArtifactListSerializer
    filter_params_serializer_class = EventArtifactListFilterSerializer
    search_fields = ("event__name", "artifact__name")

    @extend_schema(
        parameters=[EventArtifactListFilterSerializer],
        responses={
            status.HTTP_200_OK: EventArtifactListSerializer(many=True),
        },
        tags=["game_world:event_artifact"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class EventArtifactDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Артефакты за выполнение события. Детальная информация.
    """

    selector = EventArtifactDetailSelector
    serializer_class = EventArtifactDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: EventArtifactDetailSerializer,
        },
        tags=["game_world:event_artifact"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        event_artifact = self.get_object()
        serializer = self.get_serializer(instance=event_artifact)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class EventArtifactCreateAPIView(GenericAPIView):
    """
    Артефакты за выполнение события. Создание.
    """

    serializer_class = EventArtifactCreateOrUpdateSerializer

    @extend_schema(
        request=EventArtifactCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: EventArtifactDetailSerializer,
        },
        tags=["game_world:event_artifact"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_artifact = serializer.save()

        return Response(
            data=EventArtifactDetailSerializer(
                instance=event_artifact,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class EventArtifactUpdateAPIView(GenericAPIView):
    """
    Артефакты за выполнение события. Изменение.
    """

    queryset = EventArtifact.objects.all()
    serializer_class = EventArtifactCreateOrUpdateSerializer

    @extend_schema(
        request=EventArtifactCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: EventArtifactDetailSerializer,
        },
        tags=["game_world:event_artifact"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        event_artifact = self.get_object()
        serializer = self.get_serializer(
            instance=event_artifact,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        event_artifact = serializer.save()
        if getattr(event_artifact, "_prefetched_objects_cache", None):
            event_artifact._prefetched_objects_cache = {}

        return Response(
            data=EventArtifactDetailSerializer(
                instance=event_artifact,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class EventArtifactDeleteAPIView(GenericAPIView):
    """
    Артефакты за выполнение события. Удаление объекта.
    """

    queryset = EventArtifact.objects.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_world:event_artifact"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        event_artifact = self.get_object()
        event_artifact.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
