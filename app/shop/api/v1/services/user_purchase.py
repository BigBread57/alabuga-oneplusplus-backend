from datetime import timedelta
from typing import Any

from django.db import transaction
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from common.services import BaseService
from game_world.models import Artifact
from shop.models import UserPurchase, ShopItem
from shop.tasks import send_mail_about_new_user_purchase
from user.models import User, Character, CharacterArtifact
from django.utils.translation import gettext_lazy as _


class UserPurchaseService(BaseService):
    """
    Покупки пользователя. Сервис.
    """

    def create(
        self,
        validated_data: dict[str, Any],
        buyer: User,
    ) -> UserPurchase:
        """
        Создание покупки пользователя.
        """
        shop_item = validated_data["shop_item"]
        number = validated_data["number"]
        with transaction.atomic():
            new_number = 0 if shop_item.number == 0 else shop_item.number - number
            if getattr(shop_item, "purchase_restriction", None) and shop_item.purchase_restriction < number:
                raise ValidationError(_("На покупку товара стоит ограничение"))

            if shop_item.number != 0 and new_number < 0:
                raise ValidationError(_("Введенное вами количество товара не доступно"))

            if shop_item.start_datetime and shop_item.time_to_buy and (shop_item.start_datetime + timedelta(hours=shop_item.time_to_buy) < now()):
                raise ValidationError(_("Время для покупки товара истекло"))

            character = Character.objects.filter(is_active=True, user=buyer).first()
            character_artifacts_shop_discount = list(
                CharacterArtifact.objects.filter(
                    character=character,
                    artifact__modifier=Artifact.Modifiers.SHOP_DISCOUNT,
                ).values_list("artifact__modifier_value")
            )
            discount = (100 - sum(character_artifacts_shop_discount)) / 100
            total_sum = number * shop_item.price * discount
            if character.currency < total_sum:
                raise ValidationError(_("У вас не достаточно денег для покупки"))

            ShopItem.objects.filter(
                id=shop_item.id,
            ).update(
                number=new_number,
                is_active=False if (new_number == 0 and shop_item.number != 0) else True,
            )

            user_purchase = UserPurchase.objects.create(
                price=shop_item.price,
                number=validated_data["number"],
                discount=discount,
                total_sum=total_sum,
                status=UserPurchase.Statuses.PENDING,
                buyer=buyer,
                shop_item=shop_item,
            )
        transaction.on_commit(
            lambda: send_mail_about_new_user_purchase.delay(user_purchase_id=user_purchase.id),
        )

        return user_purchase

    def update(
        self,
        user_purchase: UserPurchase,
        validated_data: dict[str, Any],
        manager: User,
    ) -> UserPurchase:
        """
        Изменение статуса покупки пользователя.
        """
        UserPurchase.objects.filter(
            id=user_purchase.id,
        ).update(
            **validated_data,
        )
        transaction.on_commit(
            lambda: send_mail_about_new_user_purchase.delay(user_purchase_id=user_purchase.id),
        )
        user_purchase.refresh_from_db()

        return user_purchase

    def to_work(
        self,
        user_purchase: UserPurchase,
        manager: User,
    ) -> None:
        """
        Создание покупки пользователя.
        """
        UserPurchase.objects.filter(
            id=user_purchase.id,
        ).update(
            manager=manager,
        )
        return None


user_purchase_service = UserPurchaseService()
