from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import User


class BaseUserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя. Используется в других сериалайзерах."""

    avatar = serializers.ImageField(use_url=True)

    class Meta:
        model = User
        fields = (
            "id",
            "avatar",
            "email",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
        )


class UseResendEmailConfirmationSerializer(serializers.Serializer):
    """
    Сериализатор отправки сообщения подтверждения регистрации.
    """

    email = serializers.EmailField(
        label=_("Email"),
        help_text=_("Email"),
        required=True,
    )

    user: User | None = None

    def validate_email(self, email: str) -> str:
        """Валидность email для восстановления пароля."""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise ValidationError(
                _("Пользователь с указанными данными не найден, проверьте email или зарегистрируйтесь")
            ) from exc

        if user.is_active:
            raise ValidationError(_("Пользователь с указанным email уже активен"))

        self.user = user
        return email


class UserLoginSerializer(serializers.Serializer):
    """Сериалайзер для авторизации пользователя."""

    email = serializers.EmailField(
        label=_("Email"),
        help_text=_("Email"),
        required=True,
    )
    password = serializers.CharField(
        label=_("Пароль"),
        help_text=_("Пароль"),
        required=True,
    )

    user: User | None = None

    def validate_email(self, email: str) -> str:
        """Валидность email для восстановления пароля."""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise ValidationError(
                _("Пользователь с указанными данными не найден, проверьте email или зарегистрируйтесь")
            ) from exc

        self.user = user
        return email


class UserRequestResetPasswordSerializer(serializers.Serializer):
    """Восстановление забытого пользователем пароля. Этап №1."""

    email = serializers.EmailField(required=True)

    user: User | None = None

    def validate_email(self, email: str) -> str:
        """Валидность email для восстановления пароля."""
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise ValidationError(_("Пользователя с таким email не существует")) from exc
        return email


class UserConfirmResetPasswordSerializer(serializers.Serializer):
    """Успешное восстановление пароля пользователя. Этап №2."""

    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs: dict[str, Any]):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 != password2:
            raise ValidationError(
                {
                    "new_password": [
                        _(
                            "Пароли должны совпадать! " + "Проверьте корректность данных",
                        ),
                    ],
                },
            )
        try:
            validate_password(str(password1))
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc


class UserUpdatePasswordSerializer(serializers.Serializer):
    """Изменение пароля."""

    password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate_password(self, password: str) -> str:
        """Проверка корректности введенного пароля."""
        user = self.context.get("request").user
        if check_password(password, user.password):
            return password
        raise ValidationError(
            {"password": [_("Вы ввели некорректный пароль")]},
        )

    def validate(self, attrs: dict[str, Any]):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 != password2:
            raise ValidationError(
                {
                    "new_password": [
                        _(
                            "Пароли должны совпадать! " + "Проверьте корректность данных",
                        ),
                    ],
                },
            )
        try:
            validate_password(str(password1))
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc


class UserRegisterSerializer(serializers.Serializer):
    """
    Регистрация пользователя.
    """

    first_name = serializers.CharField(label=_("Имя"), help_text=_("Имя"), required=True)
    last_name = serializers.CharField(label=_("Отчество"), help_text=_("Отчество"), required=True)
    middle_name = serializers.CharField(label=_("Фамилия"), help_text=_("Фамилия"), required=True)
    email = serializers.EmailField(label=_("Email"), help_text=_("Email"), required=True)
    phone = serializers.EmailField(label=_("Телефон"), help_text=_("Телефон"), required=True)
    password1 = serializers.CharField(
        label=_("Пароль 1"),
        help_text=_("Пароль 1"),
        required=True,
    )
    password2 = serializers.CharField(
        label=_("Пароль 2"),
        help_text=_("Пароль 2"),
        required=True,
    )

    def validate_email(self, email: str) -> None:
        """Валидация email."""
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                {
                    "email": [
                        _(
                            f"Пользователь с email {email} "
                            + "уже существует, укажите другой email или "
                            + "попробуйте восстановить пароль.",
                        )
                    ],
                },
            )

    def validate(self, attrs: dict[str, Any]):
        """Валидация паролей."""
        password1 = attrs["password1"]
        password2 = attrs["password2"]

        if not password1:
            raise ValidationError(
                {"password1": [_("Необходимо указать пароль")]},
            )

        if not password2:
            raise ValidationError(
                {"password2": [_("Необходимо указать пароль два раза")]},
            )

        if password1 != password2:
            raise ValidationError(
                {"password": [_("Оба пароля должны совпадать")]},
            )

        try:
            validate_password(str(password1))
        except DjangoValidationError as exc:
            raise ValidationError(exc.messages) from exc


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Пользователь. Детальная информация об авторизованном пользователе.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
            "is_active",
        )
