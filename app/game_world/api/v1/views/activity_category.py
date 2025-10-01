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
    ActivityCategoryDetailSelector,
    ActivityCategoryListFilterSerializer,
    ActivityCategoryListSelector,
)
from game_world.api.v1.serializers import (
    ActivityCategoryCreateOrUpdateSerializer,
    ActivityCategoryDetailSerializer,
    ActivityCategoryListSerializer,
)
from game_world.models import ActivityCategory


class ActivityCategoryListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Категория миссии. Список.
    """

    selector = ActivityCategoryListSelector
    serializer_class = ActivityCategoryListSerializer
    filter_params_serializer_class = ActivityCategoryListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[ActivityCategoryListFilterSerializer],
        responses={
            status.HTTP_200_OK: ActivityCategoryListSerializer(many=True),
        },
        tags=["game_world:activity_category"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class ActivityCategoryDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Категория миссии. Детальная информация.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    selector = ActivityCategoryDetailSelector
    serializer_class = ActivityCategoryDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: ActivityCategoryDetailSerializer,
        },
        exclude=True,
        tags=["game_world:activity_category"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        activity_category = self.get_object()
        serializer = self.get_serializer(instance=activity_category)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class ActivityCategoryCreateAPIView(GenericAPIView):
    """
    Категория миссии. Создание.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    serializer_class = ActivityCategoryCreateOrUpdateSerializer
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        request=ActivityCategoryCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: ActivityCategoryDetailSerializer,
        },
        exclude=True,
        tags=["game_world:activity_category"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activity_category = serializer.save()

        return Response(
            data=ActivityCategoryDetailSerializer(
                instance=activity_category,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class ActivityCategoryUpdateAPIView(GenericAPIView):
    """
    Категория миссии. Изменение.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = ActivityCategory.objects.all()
    serializer_class = ActivityCategoryCreateOrUpdateSerializer
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        request=ActivityCategoryCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: ActivityCategoryDetailSerializer,
        },
        exclude=True,
        tags=["game_world:activity_category"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        activity_category = self.get_object()
        serializer = self.get_serializer(
            instance=activity_category,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        activity_category = serializer.save()
        if getattr(activity_category, "_prefetched_objects_cache", None):
            activity_category._prefetched_objects_cache = {}

        return Response(
            data=ActivityCategoryDetailSerializer(
                instance=activity_category,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class ActivityCategoryDeleteAPIView(GenericAPIView):
    """
    Категория миссии. Удаление объекта.
    """

    queryset = ActivityCategory.objects.all()
    permission_classes = (CharacterHrPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        exclude=True,
        tags=["game_world:activity_category"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        activity_category = self.get_object()
        activity_category.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
