from datetime import timedelta
from typing import Any

from django.db import models, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from common.services import BaseService
from game_world.models import Artifact
from shop.models import CharacterPurchase, ShopItem
from shop.tasks import send_mail_about_new_character_purchase
from user.models import Character, CharacterArtifact, User


class CharacterPurchaseService(BaseService):
    """
    Покупки пользователя. Сервис.
    """

    def create(
        self,
        validated_data: dict[str, Any],
        buyer: Character,
    ) -> CharacterPurchase:
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

            if (
                shop_item.start_datetime
                and shop_item.time_to_buy
                and (shop_item.start_datetime + timedelta(hours=shop_item.time_to_buy) < now())
            ):
                raise ValidationError(_("Время для покупки товара истекло"))

            character_artifacts_shop_discount = list(
                CharacterArtifact.objects.filter(
                    character=buyer,
                    artifact__modifier=Artifact.Modifiers.SHOP_DISCOUNT,
                ).values_list("artifact__modifier_value", flat=True)
            )
            discount = (100 - sum(character_artifacts_shop_discount)) / 100
            total_sum = number * shop_item.price * discount
            if buyer.currency < total_sum:
                raise ValidationError(_("У вас не достаточно денег для покупки"))

            ShopItem.objects.filter(
                id=shop_item.id,
            ).update(
                number=new_number,
                is_active=(False if (new_number == 0 and shop_item.number != 0) else True),
            )

            character_purchase = CharacterPurchase.objects.create(
                price=shop_item.price,
                number=validated_data["number"],
                discount=discount,
                total_sum=total_sum,
                status=CharacterPurchase.Statuses.PENDING,
                buyer=buyer,
                shop_item=shop_item,
            )
            Character.objects.filter(
                id=buyer.id,
            ).update(
                currency=models.F("currency") - total_sum,
            )

        transaction.on_commit(
            lambda: send_mail_about_new_character_purchase.delay(character_purchase_id=character_purchase.id),
        )

        return character_purchase

    def update(
        self,
        character_purchase: CharacterPurchase,
        validated_data: dict[str, Any],
    ) -> CharacterPurchase:
        """
        Изменение статуса покупки пользователя.
        """
        CharacterPurchase.objects.filter(
            id=character_purchase.id,
        ).update(
            **validated_data,
        )
        transaction.on_commit(
            lambda: send_mail_about_new_character_purchase.delay(character_purchase_id=character_purchase.id),
        )
        character_purchase.refresh_from_db()

        return character_purchase

    def to_work(
        self,
        character_purchase: CharacterPurchase,
        manager: User,
    ) -> None:
        """
        Создание покупки пользователя.
        """
        CharacterPurchase.objects.filter(
            id=character_purchase.id,
        ).update(
            manager=manager,
        )
        return None


character_purchase_service = CharacterPurchaseService()
