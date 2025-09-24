from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from mission_branch.api.v1.selectors import (
    MissionBranchListFilterSerializer,
    MissionBranchListSelector,
)
from mission_branch.api.v1.serializers import (
    MissionBranchCreateOrUpdateSerializer,
    MissionBranchDetailSerializer,
    MissionBranchListSerializer,
)
from mission_branch.models import MissionBranch
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import UserHRPermission
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin


class MissionBranchListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Ветка миссии. Список.
    """

    selector = MissionBranchListSelector
    serializer_class = MissionBranchListSerializer
    filter_params_serializer_class = MissionBranchListFilterSerializer
    search_fields = ("name",)

    @extend_schema(
        parameters=[MissionBranchListFilterSerializer],
        responses={
            status.HTTP_200_OK: MissionBranchListSerializer(many=True),
        },
        tags=["mission_branch:mission_branch"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class MissionBranchDetailAPIView(GenericAPIView):
    """
    Ветка миссии. Детальная информация.
    """

    selector = MissionBranch.objects.all()
    serializer_class = MissionBranchDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: MissionBranchDetailSerializer,
        },
        tags=["mission_branch:user_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        user_purchase = self.get_object()
        serializer = self.get_serializer(instance=user_purchase)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class MissionBranchCreateAPIView(GenericAPIView):
    """
    Ветка миссии. Создание.
    """

    serializer_class = MissionBranchCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=MissionBranchCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: MissionBranchDetailSerializer,
        },
        tags=["mission_branch:mission_branch"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mission_branch = serializer.save()

        return Response(
            data=MissionBranchDetailSerializer(
                instance=mission_branch,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class MissionBranchUpdateAPIView(GenericAPIView):
    """
    Ветка миссии. Изменение.
    """

    queryset = MissionBranch.objects.all()
    serializer_class = MissionBranchCreateOrUpdateSerializer
    permission_classes = (UserHRPermission,)

    @extend_schema(
        request=MissionBranchCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: MissionBranchDetailSerializer,
        },
        tags=["mission_branch:mission_branch"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        placement_metering_device = self.get_object()
        serializer = self.get_serializer(
            instance=placement_metering_device,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        mission_branch = serializer.save()
        if getattr(mission_branch, "_prefetched_objects_cache", None):
            mission_branch._prefetched_objects_cache = {}

        return Response(
            data=MissionBranchDetailSerializer(
                instance=placement_metering_device,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class MissionBranchDeleteAPIView(GenericAPIView):
    """
    Ветка миссии. Удаление объекта.
    """

    queryset = MissionBranch.objects.all()
    permission_classes = (UserHRPermission,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["mission_branch:mission_branch"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        mission_branch = self.get_object()
        mission_branch.delete()

        return Response(
            data=ResponseDetailSerializer(detail={"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
