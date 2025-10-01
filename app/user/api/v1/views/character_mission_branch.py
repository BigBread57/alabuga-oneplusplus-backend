from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.views import QuerySelectorMixin
from user.api.v1.selectors import (
    CharacterMissionBranchListFilterSerializer,
    CharacterMissionBranchListSelector,
)
from user.api.v1.serializers import CharacterMissionBranchListSerializer


class CharacterMissionBranchListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Ветка миссии персонажа. Список.
    """

    selector = CharacterMissionBranchListSelector
    serializer_class = CharacterMissionBranchListSerializer
    filter_params_serializer_class = CharacterMissionBranchListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[CharacterMissionBranchListFilterSerializer],
        responses={
            status.HTTP_200_OK: CharacterMissionBranchListSerializer(many=True),
        },
        tags=["user:character_branches_mission"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)
