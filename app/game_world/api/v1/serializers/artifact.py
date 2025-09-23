from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.models import Artifact


class ArtifactListSerializer(serializers.ModelSerializer):
    """
    Артефакт. Список.
    """

    modifier_display_name = serializers.SerializerMethodField(
        label=_("Название статуса"),
        help_text=_("Название статуса"),
    )

    class Meta:
        model = Artifact
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "modifier",
            "modifier_display_name",
            "modifier_value",
        )

    def get_modifier_display_name(self, artifact: Artifact) -> str:
        """
        Название статуса.
        """
        return artifact.get_modifier_display()


class ArtifactDetailSerializer(serializers.ModelSerializer):
    """
    Артефакт. Детальная информация.
    """

    modifier_display_name = serializers.SerializerMethodField(
        label=_("Название статуса"),
        help_text=_("Название статуса"),
    )

    class Meta:
        model = Artifact
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "modifier",
            "modifier_display_name",
            "modifier_value",
        )

    def get_modifier_display_name(self, artifact: Artifact) -> str:
        """
        Название статуса.
        """
        return artifact.get_modifier_display()


class ArtifactCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Артефакт. Создание.
    """

    class Meta:
        model = Artifact
        fields = (
            "name",
            "description",
            "icon",
            "modifier",
            "modifier_value",
        )
