from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from communication.api.v1.serializers import CommentCreateSerializer, CommentListOrDetailSerializer


class CommentCreateAPIView(GenericAPIView):
    """
    Комментарий. Создание.
    """

    serializer_class = CommentCreateSerializer

    @extend_schema(
        request=CommentCreateSerializer,
        responses={
            status.HTTP_201_CREATED: CommentListOrDetailSerializer,
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
            data=CommentListOrDetailSerializer(
                instance=comment,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )
