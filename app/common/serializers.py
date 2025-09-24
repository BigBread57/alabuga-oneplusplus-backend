from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ResponseDetailSerializer(serializers.Serializer):
    """Подробная информация в Response."""

    detail = serializers.CharField(
        label=_("Подробная информация о результате действия"),
        help_text=_("Подробная информация о результате действия"),
        required=True,
    )


class CurrentCharacterDefault:
    """
    Возвращает персонажа текущего пользователя по умолчанию.
    """

    requires_context = True

    def __call__(self, serializer_field):
        user = serializer_field.context["request"].user
        if hasattr(user, "character"):
            return user.character
        return None
