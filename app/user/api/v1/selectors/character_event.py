import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from common.constants import UserRoles
from common.selectors import BaseSelector, CurrentCharacterDefault
from user.models import CharacterEvent, User


class CharacterEventListFilterSerializer(serializers.Serializer):
    """
    Событие персонажа. Список. Сериализатор для фильтра.
    """

    status = serializers.ChoiceField(
        label=_("Статус"),
        help_text=_("Статус"),
        choices=CharacterEvent.Statuses.choices,
        required=True,
    )
    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class CharacterEventDetailOrUpdateFilterSerializer(serializers.Serializer):
    """
    Событие персонажа. Детальная информация/изменение со стороны персонажа. Сериализатор для фильтра.
    """

    character = serializers.HiddenField(
        label=_("Персонаж"),
        help_text=_("Персонаж"),
        default=CurrentCharacterDefault(),
    )


class CharacterEventForInspectorFilterSerializer(serializers.Serializer):
    """
    Событие персонажа. Детальная информация/изменение со стороны проверяющего. Сериализатор для фильтра.
    """

    inspector = serializers.HiddenField(
        label=_("Проверяющий"),
        help_text=_("Проверяющий"),
        default=CurrentUserDefault(),
    )


class CharacterEventListFilter(django_filters.FilterSet):
    """
    Событие персонажа. Список. Фильтр.
    """

    class Meta:
        model = CharacterEvent
        fields = ("status", "character")


class CharacterEventDetailOrUpdateFilter(django_filters.FilterSet):
    """
    Событие персонажа. Детальная информация/изменение со стороны персонажа. Фильтр.
    """

    class Meta:
        model = CharacterEvent
        fields = ("character",)


class CharacterEventDetailForInspectorFilter(django_filters.FilterSet):
    """
    Событие персонажа. Детальная информация/изменение со стороны проверяющего. Фильтр.
    """

    inspector = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_("Проверяющий"),
        help_text=_("Проверяющий"),
        method="inspector_filter",
    )

    class Meta:
        model = CharacterEvent
        fields = ("inspector",)

    def inspector_filter(self, queryset, name, value):
        """
        Фильтр по проверяющему.
        """
        if getattr(value, "role", None) == UserRoles.HR:
            return queryset.all()
        return queryset.filter(inspector=value)


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


class CharacterEventDetailSelector(BaseSelector):
    """
    Событие персонажа. Детальная информация. Селектор.
    """

    queryset = CharacterEvent.objects.all()
    filter_class = CharacterEventDetailOrUpdateFilter


class CharacterEventUpdateFromCharacterSelector(BaseSelector):
    """
    Событие персонажа. Изменение со стороны персонажа. Селектор.
    """

    queryset = CharacterEvent.objects.all()
    filter_class = CharacterEventDetailOrUpdateFilter


class CharacterEventUpdateFromInspectorSelector(BaseSelector):
    """
    Событие персонажа. Изменение со стороны проверяющего. Селектор.
    """

    queryset = CharacterEvent.objects.all()
    filter_class = CharacterEventDetailOrUpdateFilter
