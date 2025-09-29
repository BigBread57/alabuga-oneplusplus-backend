import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from common.selectors import BaseSelector
from game_world.models import Artifact
from user.models import Character, CharacterEvent, CharacterMission


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


class CharacterStatisticsSelector(BaseSelector):
    """
    Персонаж пользователя. Статистика. Селектор.
    """

    queryset = Character.objects.prefetch_related(
        "character_missions__mission__level",
        "character_missions__mission__category",
        "character_events__event__category",
        "character_artifacts__artifact",
        "character_competencies__competency",
    ).annotate(
        # Mission
        total_missions=models.Count("character_missions__id", distinct=True),
        completed_missions=models.Count(
            "character_missions__id",
            filter=models.Q(character_missions__status=CharacterMission.Statuses.COMPLETED),
            distinct=True,
        ),
        in_progress_missions=models.Count(
            "character_missions__id",
            filter=models.Q(character_missions__status=CharacterMission.Statuses.IN_PROGRESS),
            distinct=True,
        ),
        need_improvement_missions=models.Count(
            "character_missions__id",
            filter=models.Q(character_missions__status=CharacterMission.Statuses.NEED_IMPROVEMENT),
            distinct=True,
        ),
        pending_review_missions=models.Count(
            "character_missions__id",
            filter=models.Q(character_missions__status=CharacterMission.Statuses.PENDING_REVIEW),
            distinct=True,
        ),
        failed_missions=models.Count(
            "character_missions__id",
            filter=models.Q(character_missions__status=CharacterMission.Statuses.FAILED),
            distinct=True,
        ),
        # Event
        total_events=models.Count("character_events__id", distinct=True),
        completed_events=models.Count(
            "character_events__id",
            filter=models.Q(character_events__status=CharacterEvent.Statuses.COMPLETED),
            distinct=True,
        ),
        in_progress_events=models.Count(
            "character_events__id",
            filter=models.Q(character_events__status=CharacterEvent.Statuses.IN_PROGRESS),
            distinct=True,
        ),
        need_improvement_events=models.Count(
            "character_events__id",
            filter=models.Q(character_events__status=CharacterEvent.Statuses.NEED_IMPROVEMENT),
            distinct=True,
        ),
        pending_review_events=models.Count(
            "character_events__id",
            filter=models.Q(character_events__status=CharacterEvent.Statuses.PENDING_REVIEW),
            distinct=True,
        ),
        failed_events=models.Count(
            "character_events__id",
            filter=models.Q(character_events__status=CharacterEvent.Statuses.FAILED),
            distinct=True,
        ),
        # Artifact
        total_artifacts=models.Count("character_artifacts__id", distinct=True),
        default_artifacts=models.Count(
            "character_artifacts__id",
            filter=models.Q(character_artifacts__artifact__modifier=Artifact.Modifiers.DEFAULT),
            distinct=True,
        ),
        experience_gain_artifacts=models.Count(
            "character_artifacts__id",
            filter=models.Q(character_artifacts__artifact__modifier=Artifact.Modifiers.EXPERIENCE_GAIN),
            distinct=True,
        ),
        currency_gain_artifacts=models.Count(
            "character_artifacts__id",
            filter=models.Q(character_artifacts__artifact__modifier=Artifact.Modifiers.CURRENCY_GAIN),
            distinct=True,
        ),
        shop_discount_artifacts=models.Count(
            "character_artifacts__id",
            filter=models.Q(character_artifacts__artifact__modifier=Artifact.Modifiers.SHOP_DISCOUNT),
            distinct=True,
        ),
        # Competence
        total_competencies=models.Count("character_competencies__id", distinct=True),
    )
