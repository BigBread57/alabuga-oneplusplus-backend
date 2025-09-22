from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.common.permissions import UserHRPermission
from app.common.serializers import ResponseDetailSerializer
from app.common.views import QuerySelectorMixin
from app.game_world.api.v1.selectors import ArtifactListFilterSerializer, ArtifactListSelector
from app.game_world.api.v1.serializers import (
    ArtifactCreateOrUpdateSerializer,
    ArtifactDetailSerializer,
    ArtifactListSerializer,
)
from app.game_world.models import Artifact


class ArtifactListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Артефакт. Список.
    """

    selector = ArtifactListSelector()
    serializer_class = ArtifactListSerializer
    filter_params_serializer_class = ArtifactListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[ArtifactListFilterSerializer],
        responses={
            status.HTTP_200_OK: ArtifactListSerializer(many=True),
        },
        tags=["game_world:artifact"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class ArtifactCreateAPIView(GenericAPIView):
    """
    Артефакт. Создание.
    """

    serializer_class = ArtifactCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=ArtifactCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: ArtifactDetailSerializer,
        },
        tags=["game_world:artifact"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artifact = serializer.save()

        return Response(
            data=ArtifactDetailSerializer(
                instance=artifact,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class ArtifactUpdateAPIView(GenericAPIView):
    """
    Артефакт. Изменение.
    """

    queryset = Artifact.objects.all()
    serializer_class = ArtifactCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=ArtifactCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: ArtifactDetailSerializer,
        },
        tags=["game_world:artifact"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        artifact = self.get_object()
        serializer = self.get_serializer(
            instance=artifact,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        artifact = serializer.save()
        if getattr(artifact, "_prefetched_objects_cache", None):
            artifact._prefetched_objects_cache = {}

        return Response(
            data=ArtifactDetailSerializer(
                instance=artifact,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class ArtifactDeleteAPIView(GenericAPIView):
    """
    Артефакт. Удаление.
    """

    queryset = Artifact.objects.all()
    permission_classes = (UserHRPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["game_world:artifact"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        artifact = self.get_object()
        artifact.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
