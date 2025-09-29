import re
from datetime import timedelta
from typing import Any

from allauth.account.forms import default_token_generator
from allauth.account.utils import url_str_to_user_pk, user_pk_to_url_str
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    NotFound,
    ParseError,
    ValidationError,
)
from rest_framework.request import Request

from common.services import BaseService
from communication.models import ActivityLog
from game_mechanics.models import Competency, Rank
from game_world.models import Event, GameWorld, Mission, MissionBranch
from user.models import (
    Character,
    CharacterCompetency,
    CharacterEvent,
    CharacterMission,
    User,
)
from user.models.character_mission_branch import CharacterMissionBranch
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
    def get_user_by_email_and_check_token(
        email: str,
        token: str,
    ):
        """Получаем пользователя по e-mail и проверяем токен."""
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise NotFound(_("Пользователь не найден")) from exc

        if not default_token_generator.check_token(user, token):
            raise ValidationError(_("Токен подтверждения регистрации не действителен"))

        return user

    @staticmethod
    def send_email_with_confirm(
        user: User,
    ) -> None:
        """
        Отправка письма со ссылкой для подтверждения регистрации.
        """
        temp_key = default_token_generator.make_token(user)
        context = {
            "user": user,
            "activate_url": f"{settings.DOMAIN_NAME}/confirm-register/?email={user.email}&token={temp_key}",
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
    ) -> None:
        """
        Запрос сброса пароля.
        """
        context = {
            "user": user,
            "password_reset_url": (
                f"{settings.DOMAIN_NAME}/request-reset-password/"
                f"{user_pk_to_url_str(user)}-{default_token_generator.make_token(user)}"
            ),
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
        self.send_email_with_confirm(user=user)
        return user

    def confirm_register(
        self,
        email: str,
        token: str,
    ) -> dict[str, Any]:
        """
        Подтверждение регистрации пользователя.
        """
        user = self.get_user_by_email_and_check_token(email=email, token=token)
        if not default_token_generator.check_token(user, token):
            raise ParseError(
                _("Некорректный ключ подтверждения активации"),
            )
        if user.is_active:
            return {"detail": _("Ваша почта уже подтверждена")}
        user.is_active = True
        user.save()

        game_world = GameWorld.objects.first()
        rank = Rank.objects.filter(game_world=game_world, parent__isnull=True).first()
        character = Character.objects.create(
            user=user,
            game_world=game_world,
        )
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
        for mission_branch in MissionBranch.objects.filter(is_active=True, rank=rank, game_world=game_world):
            character_mission_branch = CharacterMissionBranch.objects.create(
                character=character,
                branch=mission_branch,
                start_datetime=now_datetime,
                end_datetime=now_datetime + timedelta(days=mission_branch.time_to_complete),
                mentor=mission_branch.mentor,
            )
            character_missions = [
                CharacterMission(
                    character=character,
                    mission=mission,
                    branch=character_mission_branch,
                    start_datetime=now_datetime,
                    end_datetime=now_datetime + timedelta(days=mission.time_to_complete),
                    mentor=(mission.mentor if mission.mentor else character_mission_branch.mentor),
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
            for competency in Competency.objects.filter(
                game_world=game_world,
                parent__isnull=True,
            )
        ]

        CharacterMission.objects.bulk_create(objs=character_missions)
        CharacterEvent.objects.bulk_create(objs=character_events)
        CharacterCompetency.objects.bulk_create(objs=character_competencies)
        return {"detail": _("Подтверждение почты прошло успешно")}


user_service = UserService()
