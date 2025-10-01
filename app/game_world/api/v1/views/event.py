from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import CharacterHrPermission
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_world.api.v1.selectors import (
    EventDetailSelector,
    EventListFilterSerializer,
    EventListSelector,
)
from game_world.api.v1.serializers import (
    EventCreateOrUpdateSerializer,
    EventDetailSerializer,
    EventListSerializer,
)
from game_world.api.v1.services import event_service
from game_world.models import Event


class EventListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Событие. Список.
    """

    selector = EventListSelector
    serializer_class = EventListSerializer
    filter_params_serializer_class = EventListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[EventListFilterSerializer],
        responses={
            status.HTTP_200_OK: EventListSerializer(many=True),
        },
        tags=["game_world:event"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class EventDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Событие. Детальная информация.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    selector = EventDetailSelector
    serializer_class = EventDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: EventDetailSerializer,
        },
        exclude=True,
        tags=["game_world:event"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        event = self.get_object()
        serializer = self.get_serializer(instance=event)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class EventCreateAPIView(GenericAPIView):
    """
    Событие. Создание.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    serializer_class = EventCreateOrUpdateSerializer
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        request=EventCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: EventDetailSerializer,
        },
        exclude=True,
        tags=["game_world:event"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()

        return Response(
            data=EventDetailSerializer(
                instance=event,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class EventUpdateAPIView(GenericAPIView):
    """
    Событие. Изменение.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = Event.objects.all()
    serializer_class = EventCreateOrUpdateSerializer
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        request=EventCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: EventDetailSerializer,
        },
        exclude=True,
        tags=["game_world:event"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        event = self.get_object()
        serializer = self.get_serializer(
            instance=event,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        if getattr(event, "_prefetched_objects_cache", None):
            event._prefetched_objects_cache = {}

        return Response(
            data=EventDetailSerializer(
                instance=event,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class EventDeleteAPIView(GenericAPIView):
    """
    Событие. Удаление объекта.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = Event.objects.all()
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        exclude=True,
        tags=["game_world:event"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        event = self.get_object()
        event.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )


class EventCheckQrCodeAPIView(GenericAPIView):
    """
    Проверка qr кода. Удаление объекта.
    """

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_world:event"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Проверка qr кода.
        """
        event_service.check_qr_code(
            character=request.user.active_character,
            query_params=request.query_params,
        )

        return Response(
            data=ResponseDetailSerializer({"detail": _("Qr code успешно считан")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
