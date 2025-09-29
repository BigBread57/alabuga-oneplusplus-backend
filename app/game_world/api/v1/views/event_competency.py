from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_world.api.v1.selectors import (
    EventCompetencyDetailSelector,
    EventCompetencyListFilterSerializer,
    EventCompetencyListSelector,
)
from game_world.api.v1.serializers import (
    EventCompetencyCreateOrUpdateSerializer,
    EventCompetencyDetailSerializer,
    EventCompetencyListSerializer,
)
from game_world.models import EventCompetency


class EventCompetencyListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Прокачка компетенций за событие. Список.
    """

    selector = EventCompetencyListSelector
    serializer_class = EventCompetencyListSerializer
    filter_params_serializer_class = EventCompetencyListFilterSerializer
    search_fields = ("event__name", "competency__name")

    @extend_schema(
        parameters=[EventCompetencyListFilterSerializer],
        responses={
            status.HTTP_200_OK: EventCompetencyListSerializer(many=True),
        },
        tags=["game_world:event_competency"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class EventCompetencyDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Прокачка компетенций за событие. Детальная информация.
    """

    selector = EventCompetencyDetailSelector
    serializer_class = EventCompetencyDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: EventCompetencyDetailSerializer,
        },
        tags=["game_world:event_competency"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        event_competency = self.get_object()
        serializer = self.get_serializer(instance=event_competency)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class EventCompetencyCreateAPIView(GenericAPIView):
    """
    Прокачка компетенций за событие. Создание.
    """

    serializer_class = EventCompetencyCreateOrUpdateSerializer

    @extend_schema(
        request=EventCompetencyCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: EventCompetencyDetailSerializer,
        },
        tags=["game_world:event_competency"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_competency = serializer.save()

        return Response(
            data=EventCompetencyDetailSerializer(
                instance=event_competency,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class EventCompetencyUpdateAPIView(GenericAPIView):
    """
    Прокачка компетенций за событие. Изменение.
    """

    queryset = EventCompetency.objects.all()
    serializer_class = EventCompetencyCreateOrUpdateSerializer

    @extend_schema(
        request=EventCompetencyCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: EventCompetencyDetailSerializer,
        },
        tags=["game_world:event_competency"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        event_competency = self.get_object()
        serializer = self.get_serializer(
            instance=event_competency,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        event_competency = serializer.save()
        if getattr(event_competency, "_prefetched_objects_cache", None):
            event_competency._prefetched_objects_cache = {}

        return Response(
            data=EventCompetencyDetailSerializer(
                instance=event_competency,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class EventCompetencyDeleteAPIView(GenericAPIView):
    """
    Прокачка компетенций за событие. Удаление объекта.
    """

    queryset = EventCompetency.objects.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_world:event_competency"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        event_competency = self.get_object()
        event_competency.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
