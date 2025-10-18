from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import CharacterHrPermission
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from game_mechanics.api.v1.selectors import (
    CompetencyListFilterSerializer,
    CompetencyListSelector, CompetencyListMaxLevelSelector,
)
from game_mechanics.api.v1.serializers import (
    CompetencyCreateOrUpdateSerializer,
    CompetencyDetailSerializer,
    CompetencyListSerializer, CompetencyListMaxLevelSerializer,
)
from game_mechanics.models import Competency


class CompetencyListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Компетенция. Список.
    """

    selector = CompetencyListSelector
    serializer_class = CompetencyListSerializer
    filter_params_serializer_class = CompetencyListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[CompetencyListFilterSerializer],
        responses={
            status.HTTP_200_OK: CompetencyListSerializer(many=True),
        },
        tags=["game_mechanics:competency"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class CompetencyListMaxLevelAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Компетенция. Список. Максимальный уровень.
    """

    selector = CompetencyListMaxLevelSelector
    serializer_class = CompetencyListMaxLevelSerializer
    filter_params_serializer_class = CompetencyListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[CompetencyListFilterSerializer],
        responses={
            status.HTTP_200_OK: CompetencyListMaxLevelSerializer(many=True),
        },
        tags=["game_mechanics:competency"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class CompetencyCreateAPIView(GenericAPIView):
    """
    Компетенция. Создание.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    serializer_class = CompetencyCreateOrUpdateSerializer
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        request=CompetencyCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: CompetencyDetailSerializer,
        },
        exclude=True,
        tags=["game_mechanics:competency"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        competency = serializer.save()

        return Response(
            data=CompetencyDetailSerializer(
                instance=competency,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class CompetencyUpdateAPIView(GenericAPIView):
    """
    Компетенция. Изменение.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = Competency.objects.all()
    serializer_class = CompetencyCreateOrUpdateSerializer
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        request=CompetencyCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: CompetencyDetailSerializer,
        },
        exclude=True,
        tags=["game_mechanics:competency"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        competency = self.get_object()
        serializer = self.get_serializer(
            instance=competency,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        competency = serializer.save()
        if getattr(competency, "_prefetched_objects_cache", None):
            competency._prefetched_objects_cache = {}

        return Response(
            data=CompetencyDetailSerializer(
                instance=competency,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class CompetencyDeleteAPIView(GenericAPIView):
    """
    Компетенция. Удаление объекта.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = Competency.objects.all()
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        exclude=True,
        tags=["game_mechanics:competency"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        competency = self.get_object()
        competency.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
