from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.views import QuerySelectorMixin
from user.api.v1.selectors import (
    CharacterMissionListFilterSerializer,
    CharacterMissionListForInspectorFilterSerializer,
    CharacterMissionListForInspectorSelector,
    CharacterMissionListSelector,
)
from user.api.v1.serializers import (
    CharacterMissionDetailSerializer,
    CharacterMissionListSerializer,
    CharacterMissionUpdateForInspectorSerializer,
    CharacterMissionUpdateFromCharacterSerializer,
)
from user.api.v1.services import character_mission_service
from user.models import CharacterMission


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
        tags=["user:character_mission"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class CharacterMissionDetailAPIView(GenericAPIView):
    """
    Миссия персонажа. Детальная информация.
    """

    queryset = CharacterMission.objects.select_related(
        "character",
        "mission",
        "inspector",
    )
    serializer_class = CharacterMissionDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterMissionDetailSerializer,
        },
        tags=["user:character_mission"],
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


class CharacterMissionUpdateFromCharacterAPIView(GenericAPIView):
    """
    Миссия персонажа. Изменение со стороны персонажа.
    """

    queryset = CharacterMission.objects.select_related(
        "character",
        "mission",
        "inspector",
    )
    serializer_class = CharacterMissionUpdateFromCharacterSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterMissionUpdateFromCharacterSerializer,
        },
        tags=["user:character_mission"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Миссия персонажа. Изменение со стороны персонажа.
        """
        character_mission = self.get_object()
        serializer = self.get_serializer(
            instance=character_mission,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        character_mission = character_mission_service.update_from_character(
            character_mission=character_mission,
            validated_data=serializer.validated_data,
        )
        if getattr(character_mission, "_prefetched_objects_cache", None):
            character_mission._prefetched_objects_cache = {}

        return Response(
            data=CharacterMissionDetailSerializer(
                instance=character_mission,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class CharacterMissionUpdateForInspectorAPIView(GenericAPIView):
    """
    Миссия персонажа. Изменение со стороны проверяющего.
    """

    queryset = CharacterMission.objects.select_related(
        "character",
        "mission",
        "inspector",
    )
    serializer_class = CharacterMissionUpdateForInspectorSerializer
    # permission_classes = (UserInspectorForObjectPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterMissionUpdateForInspectorSerializer,
        },
        tags=["user:character_mission"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Миссия персонажа. Изменение со стороны проверяющего.
        """
        character_mission = self.get_object()
        serializer = self.get_serializer(
            instance=character_mission,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        character_mission = character_mission_service.update_from_inspector(
            character_mission=character_mission,
            validated_data=serializer.validated_data,
        )
        if getattr(character_mission, "_prefetched_objects_cache", None):
            character_mission._prefetched_objects_cache = {}

        return Response(
            data=CharacterMissionDetailSerializer(
                instance=character_mission,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class CharacterMissionListForInspectorAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Миссия персонажа для проверяющего. Список.
    """

    selector = CharacterMissionListForInspectorSelector
    serializer_class = CharacterMissionListSerializer
    filter_params_serializer_class = CharacterMissionListForInspectorFilterSerializer
    search_fields = ("name",)
    # permission_classes = (UserInspectorForObjectPermission,)

    @extend_schema(
        parameters=[CharacterMissionListForInspectorFilterSerializer],
        responses={
            status.HTTP_200_OK: CharacterMissionListSerializer(many=True),
        },
        tags=["user:character_mission"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)
