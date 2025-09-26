from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from communication.api.v1.serializers import PostListSerializer
from communication.models import Post


class PostListAPIView(GenericAPIView):
    """
    Тема. Список.
    """

    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    search_fields = ("name",)

    @extend_schema(
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
