from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_world.api.v1.selectors import (
    GameWorldStoryDetailSelector,
    GameWorldStoryListFilterSerializer,
    GameWorldStoryListSelector,
)
from game_world.api.v1.serializers import (
    GameWorldStoryCreateOrUpdateSerializer,
    GameWorldStoryDetailSerializer,
    GameWorldStoryListSerializer,
)
from game_world.models import GameWorldStory


class GameWorldStoryListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    История игрового мира. Список.
    """

    selector = GameWorldStoryListSelector
    serializer_class = GameWorldStoryListSerializer
    filter_params_serializer_class = GameWorldStoryListFilterSerializer
    search_fields = ("text", "game_world__name")

    @extend_schema(
        parameters=[GameWorldStoryListFilterSerializer],
        responses={
            status.HTTP_200_OK: GameWorldStoryListSerializer(many=True),
        },
        tags=["game_world:game_world_story"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class GameWorldStoryDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    История игрового мира. Детальная информация.
    """

    selector = GameWorldStoryDetailSelector
    serializer_class = GameWorldStoryDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: GameWorldStoryDetailSerializer,
        },
        tags=["game_world:game_world_story"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        game_world_story = self.get_object()
        serializer = self.get_serializer(instance=game_world_story)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class GameWorldStoryCreateAPIView(GenericAPIView):
    """
    История игрового мира. Создание.
    """

    serializer_class = GameWorldStoryCreateOrUpdateSerializer

    @extend_schema(
        request=GameWorldStoryCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: GameWorldStoryDetailSerializer,
        },
        tags=["game_world:game_world_story"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game_world_story = serializer.save()

        return Response(
            data=GameWorldStoryDetailSerializer(
                instance=game_world_story,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class GameWorldStoryUpdateAPIView(GenericAPIView):
    """
    История игрового мира. Изменение.
    """

    queryset = GameWorldStory.objects.all()
    serializer_class = GameWorldStoryCreateOrUpdateSerializer

    @extend_schema(
        request=GameWorldStoryCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: GameWorldStoryDetailSerializer,
        },
        tags=["game_world:game_world_story"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        game_world_story = self.get_object()
        serializer = self.get_serializer(
            instance=game_world_story,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        game_world_story = serializer.save()
        if getattr(game_world_story, "_prefetched_objects_cache", None):
            game_world_story._prefetched_objects_cache = {}

        return Response(
            data=GameWorldStoryDetailSerializer(
                instance=game_world_story,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class GameWorldStoryDeleteAPIView(GenericAPIView):
    """
    История игрового мира. Удаление объекта.
    """

    queryset = GameWorldStory.objects.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_world:game_world_story"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        game_world_story = self.get_object()
        game_world_story.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
