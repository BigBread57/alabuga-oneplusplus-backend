from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import CharacterContentManagerPermission
from common.serializers import ResponseDetailSerializer
from common.views import QuerySelectorMixin
from communication.api.v1.selectors import (
    CommentListFilterSerializer,
    CommentListSelector,
)
from communication.api.v1.serializers import (
    CommentCreateOrUpdateSerializer,
    CommentDetailSerializer,
    CommentListSerializer,
)
from communication.models import Comment


class CommentListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Комментарий. Список.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    selector = CommentListSelector
    serializer_class = CommentListSerializer
    filter_params_serializer_class = CommentListFilterSerializer
    search_fields = ("text",)

    @extend_schema(
        parameters=[CommentListFilterSerializer],
        responses={
            status.HTTP_200_OK: CommentListSerializer(many=True),
        },
        tags=["communication:comment"],
        exclude=True,
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class CommentCreateAPIView(GenericAPIView):
    """
    Комментарий. Создание.
    """

    serializer_class = CommentCreateOrUpdateSerializer
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        request=CommentCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: CommentDetailSerializer,
        },
        tags=["communication:comment"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        return Response(
            data=CommentDetailSerializer(
                instance=comment,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class CommentUpdateAPIView(GenericAPIView):
    """
    Комментарий. Изменение.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentCreateOrUpdateSerializer
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        request=CommentCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: CommentDetailSerializer,
        },
        tags=["communication:comment"],
        exclude=True,
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        comment = self.get_object()
        serializer = self.get_serializer(
            instance=comment,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        if getattr(comment, "_prefetched_objects_cache", None):
            comment._prefetched_objects_cache = {}

        return Response(
            data=CommentDetailSerializer(
                instance=comment,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class CommentDeleteAPIView(GenericAPIView):
    """
    Комментарий. Удаление объекта.

    ПОКА НЕ ИСПОЛЬЗУЕТСЯ.
    """

    queryset = Comment.objects.all()
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=["communication:comment"],
        exclude=True,
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        comment = self.get_object()
        comment.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
