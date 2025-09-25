import re
from datetime import timedelta
from typing import Any

from allauth.account.forms import default_token_generator
from allauth.account.utils import url_str_to_user_pk, user_pk_to_url_str
from allauth.utils import build_absolute_uri
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound, ParseError, ValidationError
from rest_framework.request import Request
from rest_framework.reverse import reverse

from common.services import BaseService
from communication.models import ActivityLog
from game_mechanics.models import Competency, Rank
from game_world.models import Event, GameWorld, Mission
from user.models import Character, CharacterCompetency, CharacterEvent, CharacterMission, User
from user.models.character_rank import CharacterRank


class SendEmailError(APIException):
    """Ошибка при отправке письма с подтверждением регистрации."""

    status_code = status.HTTP_501_NOT_IMPLEMENTED


class UserService(BaseService):
    """
    Пользователь. Сервис.
    """

    @staticmethod
    def get_user_by_token(
        pk_str: str,
        key: str,
    ) -> User:
        """Получение пользователя по ключу и id пользователя."""
        pk = url_str_to_user_pk(pk_str)

        try:
            reset_user = User.objects.get(pk=pk)
        except (ValueError, User.DoesNotExist) as exc:
            raise NotFound(_("Пользователь не найден")) from exc

        invalid_token = not default_token_generator.check_token(
            reset_user,
            key,
        )
        if reset_user is None or invalid_token:
            raise ValidationError(_("Токен сброса пароля не действителен"))
        return reset_user

    @staticmethod
    def check_extra_path(
        extra_path: str,
    ) -> tuple[str, ...]:
        """Проверка корректности extra_path, при подтверждении почты."""
        match = re.compile("(?P<email>.+)/(?P<key>.+)").match(extra_path)
        if match:
            return match.groups()

        raise ParseError(
            _(
                "Не удалось извлечь email пользователя и ключ для " + "подтверждения email",
            ),
        )

    @staticmethod
    def get_user_by_email_and_check_token(
        email: str,
        key: str,
    ):
        """Получаем пользователя по e-mail и проверяем токен."""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise NotFound(_("Пользователь не найден")) from exc

        if not default_token_generator.check_token(user, key):
            raise ValidationError(_("Токен подтверждения регистрации не действителен"))

        return user

    @staticmethod
    def send_email_with_confirm(
        user: User,
        request: Request,
    ) -> None:
        """
        Отправка письма со ссылкой для подтверждения регистрации.
        """
        temp_key = default_token_generator.make_token(user)
        path = reverse(
            viewname="user:v1:users-confirm-register",
            kwargs={"extra_path": f"{user.email}/{temp_key}"},
        )
        url = build_absolute_uri(request, path)
        url_without_api = url.replace("api/user/users/", "")

        context = {
            "user": user,
            "activate_url": url_without_api,
            "year": now().year,
            "company": "ALABUGA",
        }
        name_template = "mail/confirm_email.html"
        template = get_template(name_template).render(context)
        try:
            send_mail(
                subject=str(_("Регистрация в ALABUGA!")),
                message="",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=template,
            )
        except Exception as exc:
            raise SendEmailError(
                detail=_("Письмо с подтверждением регистрации не отправлено. Обратитесь в поддержку системы."),
            ) from exc

    @staticmethod
    def send_email_with_request_reset_password(
        user: User,
        request: Request,
    ) -> None:
        """
        Запрос сброса пароля.
        """
        path = reverse(
            viewname="user:v1:users-request-reset-password",
            kwargs={
                "extra_path": f"{user_pk_to_url_str(user)}-" + str(default_token_generator.make_token(user)),
            },
        )
        url = build_absolute_uri(request, path)
        url_without_api = url.replace("api/user/users", "")

        context = {
            "user": user,
            "password_reset_url": url_without_api,
            "year": now().year,
            "company": "ALABUGA",
        }
        name_template = "mail/reset_password.html"
        template = get_template(name_template).render(context)

        send_mail(
            subject=_("Сброс пароля"),
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=template,
        )

    @staticmethod
    def update_password(
        user: User,
        validated_data: dict[str, Any],
    ) -> None:
        """
        Смена пароля.
        """
        user.set_password(validated_data.get("new_password1"))
        user.save()
        return None

    @staticmethod
    def login(
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
        except Exception as exc:
            raise NotFound(_("Пользователь с указанными данными не найден")) from exc
        return user

    @staticmethod
    def set_new_password(
        user: User,
        password: str,
    ) -> None:
        """Установка нового пароля для пользователя."""
        user.set_password(password)
        if not user.is_active:
            user.is_active = True

        user.save()
        return None

    def get_user_reset_password_process(
        self,
        extra_path: str,
    ) -> User:
        """
        Проверка валидности токена сброса пароля.
        """
        match = re.compile("(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)").match(extra_path)
        if match:
            pk_str, key = match.groups()
            return self.get_user_by_token(pk_str, key)

        raise ValidationError(
            _("Не удалось извлечь id пользователя и ключ сброса пароля"),
        )

    def register_user(
        self,
        request: Request,
        validated_data: dict[str, Any],
    ) -> User:
        """
        Регистрация пользователя.
        """
        user = User.objects.create(
            username=validated_data["email"].split("@")[0],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            middle_name=validated_data["middle_name"],
            phone=validated_data["phone"],
            is_active=False,
        )

        # Устанавливаем пароль.
        user.set_password(validated_data.get("password1"))
        user.save()
        user.refresh_from_db()

        # Отправляем письмо активации пользователя
        self.send_email_with_confirm(
            request=request,
            user=user,
        )
        return user

    def confirm_register(
        self,
        extra_path: str,
    ) -> dict[str, Any]:
        """
        Подтверждение регистрации пользователя.
        """
        email, key = self.check_extra_path(extra_path)
        user = self.get_user_by_email_and_check_token(email=email, key=key)
        if not default_token_generator.check_token(user, key):
            raise ParseError(
                _("Некорректный ключ подтверждения активации"),
            )
        if user.is_active:
            return {"detail": _("Ваша почта уже подтверждена")}
        user.is_active = True
        user.save()

        game_world = GameWorld.objects.first()
        rank = Rank.objects.filter(game_world=game_world, parent__isnull=True)
        character = Character.objects.create(user=user)
        ActivityLog.objects.create(
            character=character,
            text=_(
                f"Добро пожаловать. Вам присвоен ранг: {rank}. "
                f"Выполняйте миссии для его повышения и получения новых наград"
            ),
            content_object=rank,
        )
        CharacterRank.objects.create(
            character=character,
            rank=rank,
        )
        now_datetime = now()
        character_missions = [
            CharacterMission(
                character=character,
                mission=mission,
                start_datetime=now_datetime,
                end_datetime=now_datetime + timedelta(days=mission.time_to_complete),
            )
            for mission in Mission.objects.filter(is_active=True, branch__rank=rank, game_world=game_world)
        ]
        character_events = [
            CharacterEvent(
                character=character,
                event=event,
                start_datetime=now_datetime,
                end_datetime=now_datetime + timedelta(days=event.time_to_complete),
            )
            for event in Event.objects.filter(is_active=True, rank=rank, game_world=game_world)
        ]
        character_competencies = [
            CharacterCompetency(
                character=character,
                competency=competency,
            )
            for competency in Competency.objects.filter(game_world=game_world)
        ]

        CharacterMission.objects.bulk_create(objs=character_missions)
        CharacterEvent.objects.bulk_create(objs=character_events)
        CharacterCompetency.objects.bulk_create(objs=character_competencies)
        return {"detail": _("Подтверждение почты прошло успешно")}


user_service = UserService()
