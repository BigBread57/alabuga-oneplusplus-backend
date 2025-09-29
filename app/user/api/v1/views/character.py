from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.views import QuerySelectorMixin
from user.api.v1.selectors import CharacterStatisticsSelector
from user.api.v1.serializers import (
    CharacterActualForUserSerializer,
    CharacterStatisticsSerializer,
    CharacterUpdateSerializer,
)
from user.api.v1.services import character_service


class CharacterActualForUserAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Персонаж пользователя. Актуальный.
    """

    serializer_class = CharacterActualForUserSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterActualForUserSerializer,
        },
        tags=["user:character"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Персонаж пользователя. Актуальный.
        """
        character = request.user.active_character
        serializer = self.get_serializer(instance=character)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class CharacterStatisticsAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Персонаж пользователя. Статистика.
    """

    selector = CharacterStatisticsSelector
    serializer_class = CharacterStatisticsSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterStatisticsSerializer,
        },
        tags=["user:character"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Персонаж пользователя. Статистика.
        """
        character = self.get_object()
        serializer = self.get_serializer(character_service.statistics(character=character))

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class CharacterActualUpdateAPIView(GenericAPIView):
    """
    Персонаж. Изменение.
    """

    serializer_class = CharacterUpdateSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterUpdateSerializer,
        },
        tags=["user:character"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Персонаж. Изменение.
        """
        character = request.user.active_character
        serializer = self.get_serializer(
            instance=character,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        character = serializer.save()
        if getattr(character, "_prefetched_objects_cache", None):
            character._prefetched_objects_cache = {}

        return Response(
            data=CharacterActualForUserSerializer(
                instance=character,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )
