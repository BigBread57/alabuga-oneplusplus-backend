from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import UserHRPermission
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_world.api.v1.selectors import (
    GameWorldListOrRatingOrStatisticsFilterSerializer,
    GameWorldListOrRatingOrStatisticsSelector,
)
from game_world.api.v1.serializers import (
    GameWorldCreateOrUpdateSerializer,
    GameWorldDetailSerializer,
    GameWorldListSerializer,
    GameWorldRatingSerializer,
    GameWorldStatisticsSerializer,
)
from game_world.api.v1.services import game_world_service
from game_world.models import GameWorld


class GameWorldListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Игровой мир. Список.
    """

    selector = GameWorldListOrRatingOrStatisticsSelector
    serializer_class = GameWorldListSerializer
    filter_params_serializer_class = GameWorldListOrRatingOrStatisticsFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[GameWorldListOrRatingOrStatisticsFilterSerializer],
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


class GameWorldDetailAPIView(GenericAPIView):
    """
    Игровой мир. Детальная информация.
    """

    queryset = GameWorld.objects.all()
    serializer_class = GameWorldDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: GameWorldDetailSerializer,
        },
        tags=["game_world:user_purchase"],
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
    """

    serializer_class = GameWorldCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=GameWorldCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: GameWorldDetailSerializer,
        },
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
    """

    queryset = GameWorld.objects.all()
    serializer_class = GameWorldCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=GameWorldCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: GameWorldDetailSerializer,
        },
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


class GameWorldDeleteAPIView(GenericAPIView):
    """
    Игровой мир. Удаление объекта.
    """

    queryset = GameWorld.objects.all()
    permission_classes = (UserHRPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
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


class GameWorldRatingAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Игровой мир. Рейтинг.
    """

    selector = GameWorldListOrRatingOrStatisticsSelector
    serializer_class = GameWorldRatingSerializer
    filter_params_serializer_class = GameWorldListOrRatingOrStatisticsFilterSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: GameWorldDetailSerializer,
        },
        tags=["game_world:user_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Рейтинг.
        """
        game_world = self.filter_queryset(queryset=self.get_queryset()).first()
        serializer = self.get_serializer(game_world_service.rating(game_world=game_world))

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class GameWorldStatisticsAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Игровой мир. Статистика.
    """

    selector = GameWorldListOrRatingOrStatisticsSelector
    serializer_class = GameWorldStatisticsSerializer
    filter_params_serializer_class = GameWorldListOrRatingOrStatisticsFilterSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: GameWorldDetailSerializer,
        },
        tags=["game_world:user_purchase"],
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
