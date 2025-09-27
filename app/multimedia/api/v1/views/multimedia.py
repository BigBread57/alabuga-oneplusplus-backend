from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from multimedia.api.v1.serializers import MultimediaCreateSerializer, MultimediaDetailSerializer


class MultimediaCreateAPIView(GenericAPIView):
    """
    Мультимедиа. Создание.
    """

    serializer_class = MultimediaCreateSerializer

    @extend_schema(
        request=MultimediaCreateSerializer,
        responses={
            status.HTTP_201_CREATED: MultimediaDetailSerializer,
        },
        tags=["game_mechanics:Multimedia"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Создание объекта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        multimedia = multimedia_service.creaate(
            character=request.user.active_character,
            validated_data=serializer.validated_data,
        )

        return Response(
            data=MultimediaDetailSerializer(
                instance=multimedia,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )
