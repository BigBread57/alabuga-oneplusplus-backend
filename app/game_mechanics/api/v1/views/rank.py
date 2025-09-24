from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import UserHRPermission
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_mechanics.api.v1.selectors import RankListFilterSerializer, RankListSelector
from game_mechanics.api.v1.serializers import RankCreateOrUpdateSerializer, RankDetailSerializer, RankListSerializer
from game_mechanics.models import Rank


class RankListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Ранг. Список.
    """

    selector = RankListSelector
    serializer_class = RankListSerializer
    filter_params_serializer_class = RankListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[RankListFilterSerializer],
        responses={
            status.HTTP_200_OK: RankListSerializer(many=True),
        },
        tags=["game_mechanics:rank"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class RankCreateAPIView(GenericAPIView):
    """
    Ранг. Создание.
    """

    serializer_class = RankCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=RankCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: RankDetailSerializer,
        },
        tags=["game_mechanics:rank"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rank = serializer.save()

        return Response(
            data=RankDetailSerializer(
                instance=rank,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class RankUpdateAPIView(GenericAPIView):
    """
    Ранг. Изменение.
    """

    queryset = Rank.objects.all()
    serializer_class = RankCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=RankCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: RankDetailSerializer,
        },
        tags=["game_mechanics:rank"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        rank = self.get_object()
        serializer = self.get_serializer(
            instance=rank,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        rank = serializer.save()
        if getattr(rank, "_prefetched_objects_cache", None):
            rank._prefetched_objects_cache = {}

        return Response(
            data=RankDetailSerializer(
                instance=rank,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class RankDeleteAPIView(GenericAPIView):
    """
    Ранг. Удаление объекта.
    """

    queryset = Rank.objects.all()
    permission_classes = (UserHRPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_mechanics:rank"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        rank = self.get_object()
        rank.delete()

        return Response(
            data=ResponseDetailSerializer(detail={"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
