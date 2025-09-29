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
    PostDetailSelector,
    PostListFilterSerializer,
    PostListSelector,
)
from communication.api.v1.serializers import (
    PostCreateOrUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
)
from communication.models import Post


class PostListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Пост. Список.
    """

    selector = PostListSelector
    serializer_class = PostListSerializer
    filter_params_serializer_class = PostListFilterSerializer
    search_fields = ("name", "text")

    @extend_schema(
        parameters=[PostListFilterSerializer],
        responses={
            status.HTTP_200_OK: PostListSerializer(many=True),
        },
        tags=["communication:post"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Список объектов.
        """
        queryset = self.filter_queryset(queryset=self.get_queryset())
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(data=serializer.data)


class PostDetailAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Пост. Детальная информация.
    """

    selector = PostDetailSelector
    serializer_class = PostDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: PostDetailSerializer,
        },
        tags=["communication:post"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        post = self.get_object()
        serializer = self.get_serializer(instance=post)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class PostCreateAPIView(GenericAPIView):
    """
    Пост. Создание.
    """

    serializer_class = PostCreateOrUpdateSerializer
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        request=PostCreateOrUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: PostDetailSerializer,
        },
        tags=["communication:post"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        return Response(
            data=PostDetailSerializer(
                instance=post,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )


class PostUpdateAPIView(GenericAPIView):
    """
    Пост. Изменение.
    """

    queryset = Post.objects.all()
    serializer_class = PostCreateOrUpdateSerializer
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        request=PostCreateOrUpdateSerializer,
        responses={
            status.HTTP_200_OK: PostDetailSerializer,
        },
        tags=["communication:post"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Изменение объекта.
        """
        post = self.get_object()
        serializer = self.get_serializer(
            instance=post,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        if getattr(post, "_prefetched_objects_cache", None):
            post._prefetched_objects_cache = {}

        return Response(
            data=PostDetailSerializer(
                instance=post,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class PostDeleteAPIView(GenericAPIView):
    """
    Пост. Удаление объекта.
    """

    queryset = Post.objects.all()
    permission_classes = (CharacterContentManagerPermission,)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        tags=["communication:post"],
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Удаление объекта.
        """
        post = self.get_object()
        post.delete()

        return Response(
            data=ResponseDetailSerializer({"detail": _("Объект успешно удален")}).data,
            status=status.HTTP_204_NO_CONTENT,
        )
