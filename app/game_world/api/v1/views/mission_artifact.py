from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_world.api.v1.selectors import (
    MissionArtifactDetailSelector,
    MissionArtifactListFilterSerializer,
    MissionArtifactListSelector,
)
from game_world.api.v1.serializers import (
    MissionArtifactCreateOrUpdateSerializer,
    MissionArtifactDetailSerializer,
    MissionArtifactListSerializer,
)
from game_world.models import MissionArtifact


class MissionArtifactListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Артефакты за выполнение миссии. Список.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    selector = MissionArtifactListSelector
    serializer_class = MissionArtifactListSerializer
    filter_params_serializer_class = MissionArtifactListFilterSerializer
    search_fields = ("mission__name", "artifact__name")

    @extend_schema(
        parameters=[MissionArtifactListFilterSerializer],
        responses={
            status.HTTP_200_OK: MissionArtifactListSerializer(many=True),
        },
        exclude=True,
        tags=["game_world:mission_artifact"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class MissionArtifactDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Артефакты за выполнение миссии. Детальная информация.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    selector = MissionArtifactDetailSelector
    serializer_class = MissionArtifactDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: MissionArtifactDetailSerializer,
        },
        exclude=True,
        tags=["game_world:mission_artifact"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        mission_artifact = self.get_object()
        serializer = self.get_serializer(instance=mission_artifact)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class MissionArtifactCreateAPIView(GenericAPIView):
    """
    Артефакты за выполнение миссии. Создание.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    serializer_class = MissionArtifactCreateOrUpdateSerializer

    @extend_schema(
        request=MissionArtifactCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: MissionArtifactDetailSerializer,
        },
        exclude=True,
        tags=["game_world:mission_artifact"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mission_artifact = serializer.save()

        return Response(
            data=MissionArtifactDetailSerializer(
                instance=mission_artifact,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class MissionArtifactUpdateAPIView(GenericAPIView):
    """
    Артефакты за выполнение миссии. Изменение.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = MissionArtifact.objects.all()
    serializer_class = MissionArtifactCreateOrUpdateSerializer

    @extend_schema(
        request=MissionArtifactCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: MissionArtifactDetailSerializer,
        },
        exclude=True,
        tags=["game_world:mission_artifact"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        mission_artifact = self.get_object()
        serializer = self.get_serializer(
            instance=mission_artifact,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        mission_artifact = serializer.save()
        if getattr(mission_artifact, "_prefetched_objects_cache", None):
            mission_artifact._prefetched_objects_cache = {}

        return Response(
            data=MissionArtifactDetailSerializer(
                instance=mission_artifact,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class MissionArtifactDeleteAPIView(GenericAPIView):
    """
    Артефакты за выполнение миссии. Удаление объекта.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = MissionArtifact.objects.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        exclude=True,
        tags=["game_world:mission_artifact"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        mission_artifact = self.get_object()
        mission_artifact.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
