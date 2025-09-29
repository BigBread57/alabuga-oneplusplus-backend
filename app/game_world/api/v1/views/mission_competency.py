from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_world.api.v1.selectors import (
    MissionCompetencyDetailSelector,
    MissionCompetencyListFilterSerializer,
    MissionCompetencyListSelector,
)
from game_world.api.v1.serializers import (
    MissionCompetencyCreateOrUpdateSerializer,
    MissionCompetencyDetailSerializer,
    MissionCompetencyListSerializer,
)
from game_world.models import MissionCompetency


class MissionCompetencyListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Прокачка компетенций за миссию. Список.
    """

    selector = MissionCompetencyListSelector
    serializer_class = MissionCompetencyListSerializer
    filter_params_serializer_class = MissionCompetencyListFilterSerializer
    search_fields = ("mission__name", "competency__name")

    @extend_schema(
        parameters=[MissionCompetencyListFilterSerializer],
        responses={
            status.HTTP_200_OK: MissionCompetencyListSerializer(many=True),
        },
        tags=["game_world:mission_competency"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class MissionCompetencyDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Прокачка компетенций за миссию. Детальная информация.
    """

    selector = MissionCompetencyDetailSelector
    serializer_class = MissionCompetencyDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: MissionCompetencyDetailSerializer,
        },
        tags=["game_world:mission_competency"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        mission_competency = self.get_object()
        serializer = self.get_serializer(instance=mission_competency)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class MissionCompetencyCreateAPIView(GenericAPIView):
    """
    Прокачка компетенций за миссию. Создание.
    """

    serializer_class = MissionCompetencyCreateOrUpdateSerializer

    @extend_schema(
        request=MissionCompetencyCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: MissionCompetencyDetailSerializer,
        },
        tags=["game_world:mission_competency"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mission_competency = serializer.save()

        return Response(
            data=MissionCompetencyDetailSerializer(
                instance=mission_competency,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class MissionCompetencyUpdateAPIView(GenericAPIView):
    """
    Прокачка компетенций за миссию. Изменение.
    """

    queryset = MissionCompetency.objects.all()
    serializer_class = MissionCompetencyCreateOrUpdateSerializer

    @extend_schema(
        request=MissionCompetencyCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: MissionCompetencyDetailSerializer,
        },
        tags=["game_world:mission_competency"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        mission_competency = self.get_object()
        serializer = self.get_serializer(
            instance=mission_competency,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        mission_competency = serializer.save()
        if getattr(mission_competency, "_prefetched_objects_cache", None):
            mission_competency._prefetched_objects_cache = {}

        return Response(
            data=MissionCompetencyDetailSerializer(
                instance=mission_competency,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class MissionCompetencyDeleteAPIView(GenericAPIView):
    """
    Прокачка компетенций за миссию. Удаление объекта.
    """

    queryset = MissionCompetency.objects.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_world:mission_competency"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        mission_competency = self.get_object()
        mission_competency.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
