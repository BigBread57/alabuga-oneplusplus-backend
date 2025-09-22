from apps.accounts.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, UserRegistrationSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class LoginAPIView(TokenObtainPairView):
    """
    Авторизация пользователя.
    """

    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Авторизация",
        description="Получение JWT токенов для авторизации",
        responses={
            200: TokenObtainPairSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshAPIView(TokenRefreshView):
    """
    Обновление JWT токена.
    """

    serializer_class = TokenRefreshSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Обновление токена",
        description="Обновление access токена с помощью refresh токена",
        responses={
            200: TokenRefreshSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegistrationAPIView(GenericAPIView):
    """
    Регистрация нового пользователя.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Регистрация",
        description="Регистрация нового пользователя в системе",
        responses={201: {"description": "Пользователь успешно создан"}, 400: {"description": "Ошибки валидации"}},
    )
    def post(self, request):
        """Регистрация пользователя."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({"message": "Пользователь успешно создан", "user_id": user.id}, status=status.HTTP_201_CREATED)
