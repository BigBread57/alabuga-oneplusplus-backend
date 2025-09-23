from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.serializers import ResponseDetailSerializer
from user.api.v1.serializers import (
    UserChangePasswordSerializer,
    UserConfirmEmailRequestSerializer,
    UserInfoSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordRequestSerializer,
)
from user.api.v1.services import user_service


class UserConfirmEmailRequestAPIView(GenericAPIView):
    """
    Повторная отправка сообщения об активации аккаунта.
    """

    serializer_class = UserConfirmEmailRequestSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserConfirmEmailRequestSerializer,
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["user:auth"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Повторная отправка сообщения об активации аккаунта.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Отправляем письмо активации пользователя
        user_service.send_confirm_email(
            user=serializer.user,
            request=request,
        )
        return Response(
            data=ResponseDetailSerializer(
                {
                    "detail": _(
                        "На указанный адрес электронной почты " + "отправлено письмо с подтверждением " + "регистрации",
                    ),
                },
            ),
            status=status.HTTP_200_OK,
        )


class UserLoginAPIView(GenericAPIView):
    """
    Авторизация пользователя.
    """

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserLoginSerializer,
        responses={
            status.HTTP_200_OK: UserInfoSerializer,
        },
        tags=["user:auth"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Авторизация пользователя.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # noqa: WPS204
        user = user_service.login(
            request=request,
            validated_data=serializer.validated_data,
        )

        return Response(
            data=UserInfoSerializer(
                instance=user,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class UserResetPasswordRequestAPIView(GenericAPIView):
    """
    Запрос сброса пароля.
    """

    serializer_class = UserResetPasswordRequestSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserResetPasswordRequestSerializer,
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["user:auth"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Запрос сброса пароля.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_service.send_email_with_reset_password(
            user=serializer.user,
            request=request,
        )
        return Response(
            data=ResponseDetailSerializer(
                {
                    "detail": _(
                        "На указанный адрес электронной почты отправлено "
                        + "письмо с инструкцией по восстановлению пароля",
                    ),
                },
            ),
            status=status.HTTP_200_OK,
        )


class UserResetPasswordConfirmAPIView(GenericAPIView):
    """
    Сброс пароля пользователя.
    """

    serializer_class = UserResetPasswordConfirmSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserResetPasswordConfirmSerializer,
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["user:auth"],
    )
    def get(self, request: Request, extra_path: str) -> Response:
        """
        Проверить возможность сброса пароля пользователя.
        """
        user = user_service.get_user_reset_password_process(extra_path)
        return Response(
            data=UserInfoSerializer(
                instance=user,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=UserResetPasswordConfirmSerializer,
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["user:auth"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Сброс пароля пользователя.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_service.set_new_password(
            extra_path=kwargs.get("extra_path"),
            password=serializer.validated_data["password1"],
        )

        return Response(
            data=ResponseDetailSerializer({"detail": _("Новый пароль успешно установлен")}),
            status=status.HTTP_200_OK,
        )


class UserChangePasswordAPIView(GenericAPIView):
    """
    Смена пароля.
    """

    serializer_class = UserChangePasswordSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserChangePasswordSerializer,
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["user:auth"],
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Смена пароля.
        """
        serializer = self.get_serializer(
            instance=request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        user_service.change_password(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            data={"detail": _("Пароль успешно изменен")},
            status=status.HTTP_200_OK,
        )


class UserRegisterAPIView(GenericAPIView):
    """
    Регистрация пользователя.
    """

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserRegisterSerializer,
        responses={
            status.HTTP_200_OK: UserInfoSerializer,
        },
        tags=["user:auth"],
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Регистрация пользователя.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_service.register_user(request=request, validated_data=serializer.validated_data)

        return Response(
            data=UserInfoSerializer(
                instance=user,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )


class UserLogoutAPIView(GenericAPIView):
    """
    Выход из системы.
    """

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: ResponseDetailSerializer,
        },
        tags=["user:auth"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Выход из системы.
        """
        logout(request=request)

        return Response(
            data=ResponseDetailSerializer({"detail": _("Пользователь успешно вышел из системы")}),
            status=status.HTTP_200_OK,
        )


class UserInfoAPIView(GenericAPIView):
    """
    Пользователь. Детальная информация об авторизованном пользователе.
    """

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={
            status.HTTP_200_OK: UserInfoSerializer,
        },
        tags=["user:auth"],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Пользователь. Детальная информация об авторизованном пользователе.
        """
        serializer = self.get_serializer(request.user)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
