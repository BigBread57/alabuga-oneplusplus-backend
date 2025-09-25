import django_filters
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from common.selectors import BaseSelector
from user.models import Character


class CharacterActualForUserFilterSerializer(serializers.Serializer):
    """
    Персонаж пользователя. Детальная информация об актуальном персонаже. Сериализатор для фильтра.
    """

    user = serializers.HiddenField(
        label=_("Пользователь"),
        help_text=_("Пользователь"),
        default=CurrentUserDefault(),
    )


class CharacterActualForUserFilter(django_filters.FilterSet):
    """
    Персонаж пользователя. Детальная информация об актуальном персонаже. Фильтр.
    """

    class Meta:
        model = Character
        fields = ("user",)


class CharacterActualForUserSelector(BaseSelector):
    """
    Персонаж пользователя. Детальная информация об актуальном персонаже. Селектор.
    """

    queryset = Character.objects.select_related(
        "user",
        "game_world",
    ).prefetch_related(
        "character_ranks",
    )
    filter_class = CharacterActualForUserFilter
