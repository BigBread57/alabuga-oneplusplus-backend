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
    GameWorldListOrStatisticsOrStatisticsFilterSerializer,
    GameWorldListOrStatisticsOrStatisticsSelector,
    GameWorldDataForGraphSelector,
)
from game_world.api.v1.serializers import (
    GameWorldCreateOrUpdateSerializer,
    GameWorldDetailSerializer,
    GameWorldGenerateSerializer,
    GameWorldInfoForGenerateSerializer,
    GameWorldListSerializer,
    GameWorldDataForGraphSerializer,
    GameWorldStatisticsSerializer,
)
from game_world.api.v1.services import game_world_service
from game_world.models import GameWorld


class GameWorldListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Игровой мир. Список.
    """

    selector = GameWorldListOrStatisticsOrStatisticsSelector
    serializer_class = GameWorldListSerializer
    filter_params_serializer_class = GameWorldListOrStatisticsOrStatisticsFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[GameWorldListOrStatisticsOrStatisticsFilterSerializer],
        responses={
            status.HTTP_200_OK: GameWorldListSerializer(many=True),
        },
        tags=["game_world:game_world"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class GameWorldDataForGraphAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Игровой мир. Список со всеми элементами.
    """

    selector = GameWorldDataForGraphSelector
    serializer_class = GameWorldDataForGraphSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: GameWorldDataForGraphSerializer,
        },
        tags=["game_world:game_world"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        game_world = self.get_object()

        return Response(
            data=game_world.data_for_graph,
            status=status.HTTP_200_OK,
        )
        # game_world = self.get_object()
        # serializer = self.get_serializer(instance=game_world)
        #
        # return Response(
        #     data=game_world_service.get_data_for_graph(
        #         game_world_data=serializer.data,
        #         data_for_graph=game_world.data_for_graph,
        #     ),
        #     status=status.HTTP_200_OK,
        # )


class GameWorldDetailAPIView(GenericAPIView):
    """
    Игровой мир. Детальная информация.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = GameWorld.objects.defer("data_for_graph")
    serializer_class = GameWorldDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: GameWorldDetailSerializer,
        },
        exclude=True,
        tags=["game_world:game_world"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        game_world = self.get_object()
        serializer = self.get_serializer(instance=game_world)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class GameWorldCreateAPIView(GenericAPIView):
    """
    Игровой мир. Создание.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    serializer_class = GameWorldCreateOrUpdateSerializer
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        request=GameWorldCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: GameWorldDetailSerializer,
        },
        exclude=True,
        tags=["game_world:game_world"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game_world = serializer.save()

        return Response(
            data=GameWorldDetailSerializer(
                instance=game_world,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class GameWorldUpdateAPIView(GenericAPIView):
    """
    Игровой мир. Изменение.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = GameWorld.objects.defer("data_for_graph")
    serializer_class = GameWorldCreateOrUpdateSerializer
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        request=GameWorldCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: GameWorldDetailSerializer,
        },
        exclude=True,
        tags=["game_world:game_world"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        game_world = self.get_object()
        serializer = self.get_serializer(
            instance=game_world,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        game_world = serializer.save()
        if getattr(game_world, "_prefetched_objects_cache", None):
            game_world._prefetched_objects_cache = {}

        return Response(
            data=GameWorldDetailSerializer(
                instance=game_world,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class GameWorldUpdateOrCreateAllEntitiesAPIView(GenericAPIView):
    """
    Игровой мир. Изменение или создание всех объектов.
    """

    queryset = GameWorld.objects.defer("data_for_graph")
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_world:game_world"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        game_world = self.get_object()
        game_world_service.update_or_create_all_entities(
            game_world=game_world,
            cells_data=request.data,
        )

        return Response(
            data=GameWorldDetailSerializer(
                instance=game_world,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class GameWorldDeleteAPIView(GenericAPIView):
    """
    Игровой мир. Удаление объекта.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = GameWorld.objects.defer("data_for_graph")
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        exclude=True,
        tags=["game_world:game_world"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        game_world = self.get_object()
        game_world.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )


class GameWorldStatisticsAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Игровой мир. Статистика.
    """

    selector = GameWorldListOrStatisticsOrStatisticsSelector
    serializer_class = GameWorldStatisticsSerializer
    filter_params_serializer_class = GameWorldListOrStatisticsOrStatisticsFilterSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: GameWorldDetailSerializer,
        },
        tags=["game_world:game_world"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Статистика.
        """
        game_world = self.filter_queryset(queryset=self.get_queryset()).first()
        serializer = self.get_serializer(game_world_service.statistics(game_world=game_world))

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class GameWorldInfoForGenerateAPIView(GenericAPIView):
    """
    Игровой мир. Информация для генерации.
    """

    queryset = GameWorld.objects.all()
    serializer_class = GameWorldInfoForGenerateSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: GameWorldInfoForGenerateSerializer(many=True),
        },
        tags=["game_world:game_world"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Информация для генерации.
        """
        serializer = self.get_serializer(game_world_service.info_for_generate(), many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class GameWorldGenerateAPIView(GenericAPIView):
    """
    Игровой мир. Генерация.
    """

    queryset = GameWorld.objects.all()
    serializer_class = GameWorldGenerateSerializer

    @extend_schema(
        # responses={
        #     status.HTTP_200_OK: GameWorldDataAfterGenerateSerializer,
        # },
        tags=["game_world:game_world"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Генерация.
        """
        game_world = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game_world_data_for_graph = game_world_service.generate(
            game_world=game_world,
            validated_data=serializer.validated_data,
        )

        return Response(
            data=game_world_data_for_graph,
            status=status.HTTP_201_CREATED,
        )
