from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from game_world.api.v1.serializers.nested import ArtifactNestedSerializer
from user.models import CharacterArtifact


class CharacterArtifactListSerializer(serializers.ModelSerializer):
    """
    Артефакт персонажа. Список.
    """

    artifact = ArtifactNestedSerializer(
        label=_("Артефакт"),
        help_text=_("Артефакт"),
    )
    content_type_id = serializers.IntegerField(
        label=_("ID тип содержимого"),
        help_text=_("ID тип содержимого"),
    )

    class Meta:
        model = CharacterArtifact
        fields = (
            "id",
            "artifact",
            "content_type_id",
            "created_at",
        )


class CharacterArtifactDetailSerializer(serializers.ModelSerializer):
    """
    Артефакт персонажа. Детальная информация.
    """

    artifact = ArtifactNestedSerializer(
        label=_("Артефакт"),
        help_text=_("Артефакт"),
    )
    content_type_id = serializers.IntegerField(
        label=_("ID тип содержимого"),
        help_text=_("ID тип содержимого"),
    )

    class Meta:
        model = CharacterArtifact
        fields = (
            "id",
            "artifact",
            "content_type_id",
            "created_at",
        )
