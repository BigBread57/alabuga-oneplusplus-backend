from rest_framework import serializers

from apps.gamification.models import Competency, UserCompetency


class CompetencyListSerializer(serializers.ModelSerializer):
    """
    Компетенция. Список объектов.
    """

    class Meta:
        model = Competency
        fields = (
            "id",
            "name",
            "description",
            "icon",
            "created_at",
        )
        
        
class UserCompetencySerializer(serializers.ModelSerializer):
    """
    Компетенция пользователя.
    """
    
    competency_name = serializers.CharField(source='competency.name', read_only=True)
    competency_icon = serializers.ImageField(source='competency.icon', read_only=True)
    
    class Meta:
        model = UserCompetency
        fields = (
            "id",
            "competency",
            "competency_name",
            "competency_icon",
            "level",
            "updated_at",
        )