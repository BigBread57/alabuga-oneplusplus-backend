from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.api.v1.serializers.nested import MissionBranchNestedSerializer
from user.models import CharacterMissionBranch


class CharacterMissionBranchListSerializer(serializers.ModelSerializer):
    """
    Ветка миссий персонажа. Список.
    """

    branch = MissionBranchNestedSerializer(
        label=_("Ветка миссий"),
        help_text=_("Ветка миссий"),
    )

    class Meta:
        model = CharacterMissionBranch
        fields = (
            "id",
            "start_datetime",
            "end_datetime",
            "start_datetime",
            "branch",
        )
