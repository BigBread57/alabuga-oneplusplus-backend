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
    CharacterCompetencyDetailOrUpdateFilterSerializer,
    CharacterCompetencyDetailSelector,
    CharacterCompetencyListFilterSerializer,
    CharacterCompetencyListSelector,
    CharacterCompetencyUpdateFromCharacterSelector,
    CharacterCompetencyUpdateFromInspectorSelector,
)
from user.api.v1.serializers import (
    CharacterCompetencyDetailSerializer,
    CharacterCompetencyListSerializer,
    CharacterCompetencyUpdateFromCharacterSerializer,
    CharacterCompetencyUpdateFromInspectorSerializer,
)
from user.api.v1.services import character_event_service


class CharacterCompetencyListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Уровень компетенции персонажа. Список.
    """

    selector = CharacterCompetencyListSelector
    serializer_class = CharacterCompetencyListSerializer
    filter_params_serializer_class = CharacterCompetencyListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[CharacterCompetencyListFilterSerializer],
        responses={
            status.HTTP_200_OK: CharacterCompetencyListSerializer(many=True),
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


class CharacterCompetencyDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Уровень компетенции персонажа. Детальная информация.
    """

    selector = CharacterCompetencyDetailSelector
    serializer_class = CharacterCompetencyDetailSerializer
    filter_params_serializer_class = CharacterCompetencyDetailOrUpdateFilterSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterCompetencyDetailSerializer,
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
