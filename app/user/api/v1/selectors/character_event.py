import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.selectors import BaseSelector, CurrentCharacterDefault
from user.models import Character, CharacterEvent


class CharacterEventForCharacterFilterSerializer(serializers.Serializer):
    """
    Событие персонажа. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class CharacterEventListFilterSerializer(CharacterEventForCharacterFilterSerializer):
    """
    Событие персонажа. Список. Сериализатор для фильтра.
    """

    status = serializers.ChoiceField(
        label=_("Статус"),
        help_text=_("Статус"),
        choices=CharacterEvent.Statuses.choices,
        required=True,
    )


class CharacterEventListForInspectorFilterSerializer(serializers.Serializer):
    """
    Событие персонажа для проверяющего. Сериализатор для фильтра.
    """

    character = serializers.PrimaryKeyRelatedField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        queryset=Character.objects.all(),
        required=False,
    )
    status = serializers.ChoiceField(
        label=_("Статус"),
        help_text=_("Статус"),
        choices=CharacterEvent.Statuses.choices,
        required=True,
    )


class CharacterEventListFilter(django_filters.FilterSet):
    """
    Событие персонажа. Список. Фильтр.
    """

    class Meta:
        model = CharacterEvent
        fields = (
            "status",
            "character",
        )


class CharacterEventListSelector(BaseSelector):
    """
    Событие персонажа. Список. Селектор.
    """

    queryset = CharacterEvent.objects.select_related(
        "character",
        "event",
        "inspector",
    )
    filter_class = CharacterEventListFilter


class CharacterEventListForInspectorSelector(BaseSelector):
    """
    Событие персонажа для проверяющего. Селектор.
    """

    filter_class = CharacterEventListFilter

    def get_queryset(self, **kwargs) -> models.QuerySet:
        active_character = self.request.user.active_character
        return CharacterEvent.objects.select_related(
            "character",
            "event",
            "inspector",
        ).exclude(
            character=active_character,
        )
