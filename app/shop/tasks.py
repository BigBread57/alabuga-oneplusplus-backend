from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from common.constants import CharacterRoles
from shop.models import CharacterPurchase
from user.models import User


@shared_task
def send_mail_about_new_character_purchase(
    character_purchase_id: int,
) -> None:
    """
    Отправить уведомление на почту менеджеру, о новой покупке.
    """
    character_purchase = CharacterPurchase.objects.select_related(
        "buyer",
        "shop_item",
    ).get(id=character_purchase_id)
    manager_emails = list(User.objects.filter(role=CharacterRoles.MANAGER).values_list("email", flat=True))
    url = "ВСТАВИТЬ ССЫЛКУ С ФРОНТА."
    send_mail(
        subject=_(f"Новая покупка №{character_purchase.id}"),
        message=(
            f"Пользователь {character_purchase.buyer.get_full_name()} совершил покупку:\n"
            f"Товар: {character_purchase.shop_item.name}\n"
            f"Цена: {character_purchase.price}\n"
            f"Количество: {character_purchase.number}\n"
            f"Общая сумма: {character_purchase.total_sum}\n"
            f"Подробнее: {url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=manager_emails,
    )
    return None


@shared_task
def send_mail_about_new_info_about_character_purchase(
    character_purchase_id: int,
) -> None:
    """
    Отправить уведомление на почту покупателю, об изменении информации по покупке.
    """
    character_purchase = CharacterPurchase.objects.select_related(
        "buyer",
        "shop_item",
    ).get(id=character_purchase_id)
    url = "ВСТАВИТЬ ССЫЛКУ С ФРОНТА."
    additional_info = (
        f"Дополнительная информация: {character_purchase.additional_info}\n"
        if character_purchase.additional_info
        else ""
    )
    send_mail(
        subject=_(f"Новая информация по вашей покупке №{character_purchase.id}"),
        message=(
            f"Менеджер {character_purchase.manager.get_full_name()} обновил информацию.\n"
            f"Товар: {character_purchase.shop_item.name}\n"
            f"Статус: {character_purchase.get_status_display()}\n"
            f"Товар: {character_purchase.shop_item.name}\n"
            f"{additional_info}"
            f"Подробнее: {url}"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[character_purchase.buyer.email],
    )
    return None
