from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from common.services import BaseService
from shop.models import UserPurchase
from shop.tasks import send_mail_about_new_user_purchase
from user.models import User


class UserPurchaseService(BaseService):
    """
    Покупки пользователя. Сервис.

    Сервис позволяет создавать/изменять/удалять покупки пользователя.
    """

    def create(
        self,
        validated_data: dict[str, Any],
        buyer: User,
    ) -> UserPurchase:
        """
        Создание покупки пользователя.
        """
        user_purchase = UserPurchase.objects.create(
            buyer=buyer,
            total_sum=validated_data["price"] * validated_data["number"],
            **validated_data,
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
        Создание покупки пользователя.
        """
        UserPurchase.objects.filter(
            id=user_purchase.id,
        ).update(
            **validated_data,
        )
        transaction.on_commit(
            lambda: send_mail_about_new_user_purchase.delay(user_purchase_id=user_purchase.id),
        )

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
