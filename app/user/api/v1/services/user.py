import re
from typing import Any

from allauth import account
from allauth.account.forms import default_token_generator
from allauth.account.internal.userkit import user_username
from allauth.account.utils import url_str_to_user_pk, user_pk_to_url_str
from allauth.utils import build_absolute_uri
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import BadRequest
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import get_template
from django.utils.timezone import now
from requests import Request
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError, APIException
from rest_framework.reverse import reverse

from app.common.services import BaseService
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class SendEmailError(APIException):
    """Ошибка при отправке письма с подтверждением регистрации."""

    status_code = status.HTTP_501_NOT_IMPLEMENTED


class UserService(BaseService):
    """
    Пользователь. Сервис.
    """

    @staticmethod
    def get_user_by_token(uidb36_inner: str, key: str) -> User:
        """Получение пользователя по ключу и id пользователя."""
        pk = url_str_to_user_pk(uidb36_inner)

        try:
            reset_user = User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist):
            raise NotFound(_('Пользователь не найден'))

        invalid_token = not default_token_generator.check_token(
            reset_user,
            key,
        )
        if reset_user is None or invalid_token:
            raise ValidationError(_('Токен сброса пароля не действителен'))
        return reset_user

    def send_confirm_email(
        self,
        user: User,
        request: Request,
    ) -> None:
        """Отправка письма со ссылкой для подтверждения регистрации."""
        temp_key = default_token_generator.make_token(user)
        path = reverse(
            viewname='api:v1:user:users-confirm-email-process',
            kwargs={'extra_path': f'{user.email}/{temp_key}'},
        )
        url = build_absolute_uri(request, path)
        url_without_api = url.replace('api/user/users/', '')

        context = {
            'user': user,
            'activate_url': url_without_api,
            'year': now().year,
            'company': 'ALABUGA',
        }
        name_template = 'email/confirm_email.html'
        template = get_template(name_template).render(context)
        try:
            send_mail(
                subject=str(_('Регистрация в ALABUGA!')),
                message="",
                recipient_list=list(user.email),
                fail_silently=False,
                html_message=template,
            )
        except Exception:
            raise SendEmailError(
                detail=_(
                    'Письмо с подтверждением регистрации не отправлено. ' +
                    'Обратитесь в поддержку системы.',
                ),
            )

    def send_email_with_reset_password(
        self,
        user: User,
        request: Request,
    ) -> None:
        """Отправка пользователю письма со сбросом пароля."""
        path = reverse(
            viewname="api:v1:user:users-reset-password-process",
            kwargs={
                'extra_path':
                    f'{user_pk_to_url_str(user)}-' +
                    str(default_token_generator.make_token(user)),
            },
        )
        url = build_absolute_uri(request, path)
        url_without_api = url.replace('api/user/users', '')

        context = {
            'current_site': get_current_site(request),
            'user': user,
            'password_reset_url': url_without_api,
            'request': request,
            'year': now().year,
        }

        method = account.app_settings.AUTHENTICATION_METHOD
        if method != account.app_settings.AuthenticationMethod.EMAIL:
            context['username'] = user_username(user)
        account.adapter.get_adapter(request).send_mail(
            'password_reset_key', user.email, context,
        )

    def login(
        self,
        request: Request,
        validated_data: dict[str, Any],
    ) -> User:
        """
        Авторизация пользователя.
        """
        try:
            user = authenticate(
                request=request,
                email=validated_data["email"],
                password=validated_data["password"],
            )
            login(
                request=request,
                user=user,
            )
        except Exception:
            raise NotFound(
                _('Пользователь с указанными данными не найден'),
            )
        return user

    def get_user_reset_password_process(self, extra_path: str) -> User:
        """
        Проверка валидности токена сброса пароля.
        """
        match = re.compile('(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)').match(extra_path)
        if match:
            uidb36, key = match.groups()
            return self.get_user_by_token(uidb36, key)

        raise ValidationError(
            _('Не удалось извлечь id пользователя и ключ сброса пароля'),
        )

    def set_new_password(self, extra_path: str, password: str) -> None:
        """Установка нового пароля для пользователя."""
        user = self.get_user_reset_password_process(extra_path=extra_path)
        user.set_password(password)

        # Активация аккаунта пользователя и создание профиля.
        if not user.is_active:
            user.is_active = True

        user.save(update_fields=['password', 'is_active'])
        return None

    def change_password(self, user: User, validated_data: dict[str, Any]) -> None:
        """
        Смена пароля.
        """
        user.set_password(validated_data.get('new_password1'))
        user.save(update_fields=['password'])
        return None


    def register_user(self, request: Request, validated_data: dict[str, Any]) -> User:
        """
        Регистрация пользователя.
        """
        user = User.objects.create(
            username=validated_data['email'].split('@')[0],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            phone=validated_data['phone'],
        )

        # Устанавливаем пароль.
        user.set_password(validated_data.get('password1'))
        user.save()
        user.refresh_from_db()

        # Отправляем письмо активации пользователя
        self.send_confirm_email(
            request=request,
            user=user,
        )
        return user

user_service = UserService()
