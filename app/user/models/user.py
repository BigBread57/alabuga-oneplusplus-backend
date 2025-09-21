from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):  # type: ignore
    """Основной класс для пользователя."""

    middle_name = models.CharField(
        verbose_name=_("Отчество"),
        max_length=50,  # noqa: WPS432
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_("Электронная почта"),
        unique=True,
    )
    phone = PhoneNumberField(
        verbose_name=_("Номер телефона"),
        blank=True,
    )
    role = models.CharField(
        verbose_name=_("Роль"),
        max_length=20,
        choices=Roles.choices,
        default=Roles.CANDIDATE,
    )

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("-id",)

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Полное имя сотрудника если он прикреплен или пользователя."""
        name_elements = (self.last_name, self.first_name, self.middle_name)
        if not any(name_elements):
            return self.username
        return " ".join(filter(None, name_elements)).strip()
