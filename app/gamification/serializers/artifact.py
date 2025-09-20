from rest_framework import serializers

from apps.gamification.models import Artifact


class ArtifactListSerializer(serializers.ModelSerializer):
    """
    Артефакт. Список объектов.
    """

    class Meta:
        model = Artifact
        fields = (
            "id",
            "name",
            "description",
            "rarity",
            "media",
            "created_at",
            "updated_at",
        )
        
        
class ArtifactDetailSerializer(serializers.ModelSerializer):
    """
    Артефакт. Детальная информация.
    """
    
    owners_count = serializers.SerializerMethodField()

    class Meta:
        model = Artifact
        fields = (
            "id",
            "name",
            "description",
            "rarity",
            "media",
            "owners_count",
            "created_at",
            "updated_at",
        )
        
    def get_owners_count(self, obj):
        """Получить количество владельцев артефакта."""
        return obj.owners.count()