from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import UserInspectorForObjectPermission
from common.views import QuerySelectorMixin
from game_mechanics.api.v1.serializers import ArtifactDetailSerializer
from user.api.v1.selectors import (
    CharacterArtifactDetailOrUpdateFilterSerializer,
    CharacterArtifactDetailSelector,
    CharacterArtifactListFilterSerializer,
    CharacterArtifactListSelector,
    CharacterArtifactUpdateFromCharacterSelector,
    CharacterArtifactUpdateFromInspectorSelector,
)
from user.api.v1.serializers import (
    CharacterArtifactDetailSerializer,
    CharacterArtifactListSerializer,
    CharacterArtifactUpdateFromCharacterSerializer,
    CharacterArtifactUpdateFromInspectorSerializer,
)
from user.api.v1.services import character_event_service


class CharacterArtifactListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Событие персонажа. Список.
    """

    selector = CharacterArtifactListSelector
    serializer_class = CharacterArtifactListSerializer
    filter_params_serializer_class = CharacterArtifactListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[CharacterArtifactListFilterSerializer],
        responses={
            status.HTTP_200_OK: CharacterArtifactListSerializer(many=True),
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


class CharacterArtifactDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Событие персонажа. Детальная информация.
    """

    selector = CharacterArtifactDetailSelector
    serializer_class = CharacterArtifactDetailSerializer
    filter_params_serializer_class = CharacterArtifactDetailOrUpdateFilterSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterArtifactDetailSerializer,
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
