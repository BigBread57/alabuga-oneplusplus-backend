from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.common.permissions import UserHRPermission
from app.common.serializers import ResponseDetailSerializer
from app.common.views import QuerySelectorMixin
from app.game_mechanics.api.v1.selectors import (
    RequiredRankCompetencyListFilterSerializer,
    RequiredRankCompetencyListSelector,
)
from app.game_mechanics.api.v1.serializers import (
    RequiredRankCompetencyCreateOrUpdateSerializer,
    RequiredRankCompetencyDetailSerializer,
    RequiredRankCompetencyListSerializer,
)
from app.game_mechanics.models import RequiredRankCompetency


class RequiredRankCompetencyListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Требования к компетенциям для получения ранга. Список.
    """

    selector = RequiredRankCompetencyListSelector()
    serializer_class = RequiredRankCompetencyListSerializer
    filter_params_serializer_class = RequiredRankCompetencyListFilterSerializer

    @extend_schema(
        parameters=[RequiredRankCompetencyListFilterSerializer],
        responses={
            status.HTTP_200_OK: RequiredRankCompetencyListSerializer(many=True),
        },
        tags=["game_mechanics:required_rank_competency"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class RequiredRankCompetencyCreateAPIView(GenericAPIView):
    """
    Требования к компетенциям для получения ранга. Создание.
    """

    serializer_class = RequiredRankCompetencyCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=RequiredRankCompetencyCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: RequiredRankCompetencyDetailSerializer,
        },
        tags=["game_mechanics:required_rank_competency"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        required_rank_competency = serializer.save()

        return Response(
            data=RequiredRankCompetencyDetailSerializer(
                instance=required_rank_competency,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class RequiredRankCompetencyUpdateAPIView(GenericAPIView):
    """
    Требования к компетенциям для получения ранга. Изменение.
    """

    queryset = RequiredRankCompetency.objects.all()
    serializer_class = RequiredRankCompetencyCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=RequiredRankCompetencyCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: RequiredRankCompetencyDetailSerializer,
        },
        tags=["game_mechanics:required_rank_competency"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        required_rank_competency = self.get_object()
        serializer = self.get_serializer(
            instance=required_rank_competency,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        required_rank_competency = serializer.save()
        if getattr(required_rank_competency, "_prefetched_objects_cache", None):
            required_rank_competency._prefetched_objects_cache = {}

        return Response(
            data=RequiredRankCompetencyDetailSerializer(
                instance=required_rank_competency,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class RequiredRankCompetencyDeleteAPIView(GenericAPIView):
    """
    Требования к компетенциям для получения ранга. Удаление.
    """

    queryset = RequiredRankCompetency.objects.all()
    permission_classes = (UserHRPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_mechanics:required_rank_competency"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        required_rank_competency = self.get_object()
        required_rank_competency.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
