from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.serializers import UserDetailSerializer, UserListSerializer, UserUpdateSerializer
from apps.common.mixins import QuerySelectorMixin

User = get_user_model()


class UserListAPIView(QuerySelectorMixin, GenericAPIView):
    """
    Список пользователей.
    """

    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    @extend_schema(
        summary="Список пользователей",
        description="Получение списка всех пользователей системы",
        responses={
            200: UserListSerializer(many=True),
        },
    )
    def get(self, request):
        """Список пользователей."""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)


class UserDetailAPIView(RetrieveUpdateAPIView):
    """
    Детальная информация о пользователе.
    """

    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UserUpdateSerializer
        return UserDetailSerializer

    @extend_schema(
        summary="Профиль пользователя",
        description="Получение детальной информации о текущем пользователе",
        responses={
            200: UserDetailSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление профиля",
        description="Обновление профиля текущего пользователя",
        request=UserUpdateSerializer,
        responses={
            200: UserDetailSerializer,
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class UserUpdateAPIView(GenericAPIView):
    """
    Обновление информации о пользователе.
    """

    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Обновление пользователя",
        description="Обновление информации о пользователе",
        responses={
            200: UserDetailSerializer,
        },
    )
    def patch(self, request):
        """Частичное обновление пользователя."""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserDetailSerializer(user, context={"request": request}).data, status=status.HTTP_200_OK)
