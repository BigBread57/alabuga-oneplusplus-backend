from rest_framework import serializers

from apps.gamification.models import Artifact, Competency
from apps.missions.models import Mission, MissionArtifact, MissionCompetency


class MissionCompetencySerializer(serializers.ModelSerializer):
    """
    Компетенции миссии.
    """
    
    competency_name = serializers.CharField(source='competency.name', read_only=True)
    
    class Meta:
        model = MissionCompetency
        fields = (
            'competency',
            'competency_name',
            'points',
        )
        

class MissionListSerializer(serializers.ModelSerializer):
    """
    Миссия. Список объектов.
    """
    
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    category = serializers.CharField(source='branch.category', read_only=True)
    
    class Meta:
        model = Mission
        fields = (
            "id",
            "name",
            "description",
            "branch",
            "branch_name",
            "category",
            "experience_reward",
            "mana_reward",
            "order",
            "is_key_mission",
            "is_active",
        )
        

class MissionDetailSerializer(serializers.ModelSerializer):
    """
    Миссия. Детальная информация.
    """
    
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    category = serializers.CharField(source='branch.category', read_only=True)
    min_rank_name = serializers.CharField(source='min_rank.name', read_only=True, allow_null=True)
    competencies = MissionCompetencySerializer(many=True, read_only=True)
    artifacts = serializers.SerializerMethodField()
    required_missions = serializers.SerializerMethodField()
    user_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Mission
        fields = (
            "id",
            "name",
            "description",
            "branch",
            "branch_name",
            "category",
            "experience_reward",
            "mana_reward",
            "min_rank",
            "min_rank_name",
            "order",
            "is_key_mission",
            "is_active",
            "competencies",
            "artifacts",
            "required_missions",
            "user_status",
            "created_at",
            "updated_at",
        )
        
    def get_artifacts(self, obj):
        """Получить артефакты миссии."""
        return [
            {
                'id': ma.artifact.id,
                'name': ma.artifact.name,
                'rarity': ma.artifact.rarity,
                'drop_chance': ma.drop_chance,
            }
            for ma in obj.missionartifact_set.select_related('artifact')
        ]
    
    def get_required_missions(self, obj):
        """Получить необходимые миссии."""
        return [
            {
                'id': mission.id,
                'name': mission.name,
            }
            for mission in obj.required_missions.all()
        ]
    
    def get_user_status(self, obj):
        """Получить статус миссии для пользователя."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_mission = obj.users.filter(user=request.user).first()
            if user_mission:
                return {
                    'status': user_mission.status,
                    'started_at': user_mission.started_at,
                    'completed_at': user_mission.completed_at,
                }
        return None


class MissionCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания миссии (для HR).
    """
    
    competencies = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )
    artifacts = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Mission
        fields = (
            "name",
            "description",
            "branch",
            "experience_reward",
            "mana_reward",
            "min_rank",
            "order",
            "is_key_mission",
            "is_active",
            "required_missions",
            "competencies",
            "artifacts",
        )
        
    def create(self, validated_data):
        """Создание миссии с компетенциями и артефактами."""
        competencies = validated_data.pop('competencies', [])
        artifacts = validated_data.pop('artifacts', [])
        required_missions = validated_data.pop('required_missions', [])
        
        mission = Mission.objects.create(**validated_data)
        
        if required_missions:
            mission.required_missions.set(required_missions)
            
        for comp_data in competencies:
            MissionCompetency.objects.create(
                mission=mission,
                competency_id=comp_data['competency_id'],
                points=comp_data.get('points', 1)
            )
            
        for art_data in artifacts:
            MissionArtifact.objects.create(
                mission=mission,
                artifact_id=art_data['artifact_id'],
                drop_chance=art_data.get('drop_chance', 1.0)
            )
            
        return mission


class MissionUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления миссии (для HR).
    """
    
    class Meta:
        model = Mission
        fields = (
            "name",
            "description",
            "experience_reward",
            "mana_reward",
            "min_rank",
            "order",
            "is_key_mission",
            "is_active",
        )