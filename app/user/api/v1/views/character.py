from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common.views import QuerySelectorMixin
from user.api.v1.selectors import CharacterActualForUserSelector
from user.api.v1.serializers import CharacterActualForUserSerializer


class CharacterActualForUserAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Персонаж пользователя. Актуальный.
    """

    selector = CharacterActualForUserSelector
    serializer_class = CharacterActualForUserSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: CharacterActualForUserSerializer,
        },
        tags=["mission:user_purchase"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Детальная информация.
        """
        character = self.filter_queryset(queryset=self.get_queryset()).first()
        serializer = self.get_serializer(instance=character)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
