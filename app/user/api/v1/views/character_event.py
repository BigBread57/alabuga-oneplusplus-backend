from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import UserInspectorForObjectPermission
from common.views import QuerySelectorMixin
from game_mechanics.api.v1.serializers import CompetencyDetailSerializer
from user.api.v1.selectors import (
    CharacterEventDetailOrUpdateFilterSerializer,
    CharacterEventDetailSelector,
    CharacterEventListFilterSerializer,
    CharacterEventListSelector,
    CharacterEventUpdateFromCharacterSelector,
    CharacterEventUpdateFromInspectorSelector,
)
from user.api.v1.serializers import (
    CharacterEventDetailSerializer,
    CharacterEventListSerializer,
    CharacterEventUpdateFromCharacterSerializer,
    CharacterEventUpdateFromInspectorSerializer,
)
from user.api.v1.services import character_event_service


class CharacterEventListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Событие персонажа. Список.
    """

    selector = CharacterEventListSelector
    serializer_class = CharacterEventListSerializer
    filter_params_serializer_class = CharacterEventListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[CharacterEventListFilterSerializer],
        responses={
            status.HTTP_200_OK: CharacterEventListSerializer(many=True),
        },
        tags=["user:character_event"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class CharacterEventDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Событие персонажа. Детальная информация.
    """

    selector = CharacterEventDetailSelector
    serializer_class = CharacterEventDetailSerializer
    filter_params_serializer_class = CharacterEventDetailOrUpdateFilterSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterEventDetailSerializer,
        },
        tags=["user:character_event"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        character_event = self.get_object()
        serializer = self.get_serializer(instance=character_event)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class CharacterEventUpdateFromCharacterAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Событие персонажа. Изменение со стороны персонажа.
    """

    selector = CharacterEventUpdateFromCharacterSelector
    serializer_class = CharacterEventUpdateFromCharacterSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterEventUpdateFromCharacterSerializer,
        },
        tags=["user:character_event"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Событие персонажа. Изменение со стороны персонажа.
        """
        character_event = self.get_object()
        serializer = self.get_serializer(
            instance=character_event,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        character_event = character_event_service.update_from_character(character_event)
        if getattr(character_event, "_prefetched_objects_cache", None):
            character_event._prefetched_objects_cache = {}

        return Response(
            data=CompetencyDetailSerializer(
                instance=character_event,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class CharacterEventUpdateFromInspectorAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Событие персонажа. Изменение со стороны проверяющего.
    """

    selector = CharacterEventUpdateFromInspectorSelector
    serializer_class = CharacterEventUpdateFromInspectorSerializer
    permission_classes = (UserInspectorForObjectPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterEventUpdateFromInspectorSerializer,
        },
        tags=["user:character_event"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Событие персонажа. Изменение со стороны проверяющего.
        """
        character_event = self.get_object()
        serializer = self.get_serializer(
            instance=character_event,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        character_event = character_event_service.update_from_inspector(character_event)
        if getattr(character_event, "_prefetched_objects_cache", None):
            character_event._prefetched_objects_cache = {}

        return Response(
            data=CompetencyDetailSerializer(
                instance=character_event,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )
