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
    CharacterMissionDetailSelector,
    CharacterMissionListFilterSerializer,
    CharacterMissionListSelector,
    CharacterMissionUpdateFromCharacterSelector,
    CharacterMissionUpdateFromInspectorSelector,
)
from user.api.v1.serializers import (
    CharacterMissionDetailSerializer,
    CharacterMissionListSerializer,
    CharacterMissionUpdateFromCharacterSerializer,
    CharacterMissionUpdateFromInspectorSerializer,
)
from user.api.v1.services import character_mission_service


class CharacterMissionListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Миссия персонажа. Список.
    """

    selector = CharacterMissionListSelector
    serializer_class = CharacterMissionListSerializer
    filter_params_serializer_class = CharacterMissionListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[CharacterMissionListFilterSerializer],
        responses={
            status.HTTP_200_OK: CharacterMissionListSerializer(many=True),
        },
        tags=["user:character_Mission"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class CharacterMissionDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Миссия персонажа. Детальная информация.
    """

    selector = CharacterMissionDetailSelector
    serializer_class = CharacterMissionDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterMissionDetailSerializer,
        },
        tags=["user:character_Mission"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        character_mission = self.get_object()
        serializer = self.get_serializer(instance=character_mission)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class CharacterMissionUpdateFromCharacterAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Миссия персонажа. Изменение со стороны персонажа.
    """

    queryset = CharacterMissionUpdateFromCharacterSelector
    serializer_class = CharacterMissionUpdateFromCharacterSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterMissionUpdateFromCharacterSerializer,
        },
        tags=["user:character_mission"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Миссия персонажа. Изменение со стороны персонажа.
        """
        character_mission = self.get_object()
        serializer = self.get_serializer(
            instance=character_mission,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        character_mission = character_mission_service.update_from_character(character_mission)
        if getattr(character_mission, "_prefetched_objects_cache", None):
            character_mission._prefetched_objects_cache = {}

        return Response(
            data=CompetencyDetailSerializer(
                instance=character_mission,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class CharacterMissionUpdateFromInspectorAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Миссия персонажа. Изменение со стороны проверяющего.
    """

    queryset = CharacterMissionUpdateFromInspectorSelector
    serializer_class = CharacterMissionUpdateFromInspectorSerializer
    permission_classes = (UserInspectorForObjectPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterMissionUpdateFromInspectorSerializer,
        },
        tags=["user:character_mission"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Миссия персонажа. Изменение со стороны проверяющего.
        """
        character_mission = self.get_object()
        serializer = self.get_serializer(
            instance=character_mission,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        character_mission = character_mission_service.update_from_inspector(character_mission)
        if getattr(character_mission, "_prefetched_objects_cache", None):
            character_mission._prefetched_objects_cache = {}

        return Response(
            data=CompetencyDetailSerializer(
                instance=character_mission,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )
