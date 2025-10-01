from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_world.api.v1.selectors import (
    MissionLevelDetailSelector,
    MissionLevelListFilterSerializer,
    MissionLevelListSelector,
)
from game_world.api.v1.serializers import (
    MissionLevelCreateOrUpdateSerializer,
    MissionLevelDetailSerializer,
    MissionLevelListSerializer,
)
from game_world.models import MissionLevel


class MissionLevelListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Уровень миссии. Список.
    """

    selector = MissionLevelListSelector
    serializer_class = MissionLevelListSerializer
    filter_params_serializer_class = MissionLevelListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[MissionLevelListFilterSerializer],
        responses={
            status.HTTP_200_OK: MissionLevelListSerializer(many=True),
        },
        tags=["game_world:mission_level"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class MissionLevelDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Уровень миссии. Детальная информация.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    selector = MissionLevelDetailSelector
    serializer_class = MissionLevelDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: MissionLevelDetailSerializer,
        },
        exclude=True,
        tags=["game_world:mission_level"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        mission_level = self.get_object()
        serializer = self.get_serializer(instance=mission_level)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class MissionLevelCreateAPIView(GenericAPIView):
    """
    Уровень миссии. Создание.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    serializer_class = MissionLevelCreateOrUpdateSerializer

    @extend_schema(
        request=MissionLevelCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: MissionLevelDetailSerializer,
        },
        exclude=True,
        tags=["game_world:mission_level"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mission_level = serializer.save()

        return Response(
            data=MissionLevelDetailSerializer(
                instance=mission_level,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class MissionLevelUpdateAPIView(GenericAPIView):
    """
    Уровень миссии. Изменение.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = MissionLevel.objects.all()
    serializer_class = MissionLevelCreateOrUpdateSerializer

    @extend_schema(
        request=MissionLevelCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: MissionLevelDetailSerializer,
        },
        exclude=True,
        tags=["game_world:mission_level"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        mission_level = self.get_object()
        serializer = self.get_serializer(
            instance=mission_level,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        mission_level = serializer.save()
        if getattr(mission_level, "_prefetched_objects_cache", None):
            mission_level._prefetched_objects_cache = {}

        return Response(
            data=MissionLevelDetailSerializer(
                instance=mission_level,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class MissionLevelDeleteAPIView(GenericAPIView):
    """
    Уровень миссии. Удаление объекта.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = MissionLevel.objects.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        exclude=True,
        tags=["game_world:mission_level"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        mission_level = self.get_object()
        mission_level.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
