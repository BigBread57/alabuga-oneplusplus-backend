from rest_framework import serializers

from apps.gamification.models import Rank, RankCompetencyRequirement


class RankCompetencyRequirementSerializer(serializers.ModelSerializer):
    """
    Требование к компетенции для ранга.
    """
    
    competency_name = serializers.CharField(source='competency.name', read_only=True)
    
    class Meta:
        model = RankCompetencyRequirement
        fields = (
            'competency',
            'competency_name',
            'level_required',
        )


class RankListSerializer(serializers.ModelSerializer):
    """
    Ранг. Список объектов.
    """

    class Meta:
        model = Rank
        fields = (
            "id",
            "name",
            "description",
            "order",
            "experience_required",
            "icon",
        )
        
        
class RankDetailSerializer(serializers.ModelSerializer):
    """
    Ранг. Детальная информация.
    """
    
    competency_requirements = RankCompetencyRequirementSerializer(many=True, read_only=True)
    required_missions_count = serializers.SerializerMethodField()

    class Meta:
        model = Rank
        fields = (
            "id",
            "name",
            "description",
            "order",
            "experience_required",
            "icon",
            "competency_requirements",
            "required_missions_count",
            "created_at",
            "updated_at",
        )
        
    def get_required_missions_count(self, obj):
        """Получить количество обязательных миссий."""
        return obj.required_missions.count()