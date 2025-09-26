from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from common.constants import CharacterRoles
from shop.models import UserPurchase
from user.models import User


@shared_task
def send_mail_about_new_user_purchase(
    user_purchase_id: int,
) -> None:
    """
    Отправить уведомление на почту менеджеру, о новой покупке.
    """
    user_purchase = UserPurchase.objects.select_related(
        "buyer",
        "shop_item",
    ).get(id=user_purchase_id)
    manager_emails = list(User.objects.filter(role=CharacterRoles.MANAGER).values_list("email", flat=True))
    url = "ВСТАВИТЬ ССЫЛКУ С ФРОНТА."
    send_mail(
        subject=_(f"Новая покупка №{user_purchase.id}"),
        message=(
            f"Пользователь {user_purchase.buyer.get_full_name()} совершил покупку:\n"
            f"Товар: {user_purchase.shop_item.name}\n"
            f"Цена: {user_purchase.price}\n"
            f"Количество: {user_purchase.number}\n"
            f"Общая сумма: {user_purchase.total_sum}\n"
            f"Подробнее: {url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=manager_emails,
    )
    return None


@shared_task
def send_mail_about_new_info_about_user_purchase(
    user_purchase_id: int,
) -> None:
    """
    Отправить уведомление на почту покупателю, об изменении информации по покупке.
    """
    user_purchase = UserPurchase.objects.select_related(
        "buyer",
        "shop_item",
    ).get(id=user_purchase_id)
    url = "ВСТАВИТЬ ССЫЛКУ С ФРОНТА."
    additional_info = (
        f"Дополнительная информация: {user_purchase.additional_info}\n" if user_purchase.additional_info else ""
    )
    send_mail(
        subject=_(f"Новая информация по вашей покупке №{user_purchase.id}"),
        message=(
            f"Менеджер {user_purchase.manager.get_full_name()} обновил информацию.\n"
            f"Товар: {user_purchase.shop_item.name}\n"
            f"Статус: {user_purchase.get_status_display()}\n"
            f"Товар: {user_purchase.shop_item.name}\n"
            f"{additional_info}"
            f"Подробнее: {url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_purchase.buyer.email],
    )
    return None
