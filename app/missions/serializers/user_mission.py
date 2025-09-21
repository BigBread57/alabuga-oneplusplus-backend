from rest_framework import serializers

from apps.missions.models import UserMission


class UserMissionSerializer(serializers.ModelSerializer):
    """
    Миссия пользователя.
    """

    mission_name = serializers.CharField(source="mission.name", read_only=True)
    mission_description = serializers.CharField(source="mission.description", read_only=True)
    mission_category = serializers.CharField(source="mission.branch.category", read_only=True)
    experience_reward = serializers.IntegerField(source="mission.experience_reward", read_only=True)
    mana_reward = serializers.IntegerField(source="mission.mana_reward", read_only=True)
    reviewed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = UserMission
        fields = (
            "id",
            "mission",
            "mission_name",
            "mission_description",
            "mission_category",
            "status",
            "started_at",
            "completed_at",
            "result",
            "review_comment",
            "reviewed_by_name",
            "experience_reward",
            "mana_reward",
            "created_at",
        )

    def get_reviewed_by_name(self, obj):
        """Получить имя проверяющего."""
        if obj.reviewed_by:
            return obj.reviewed_by.get_full_name() or obj.reviewed_by.username
        return None


class UserMissionSubmitSerializer(serializers.ModelSerializer):
    """
    Сериализатор отправки результата миссии.
    """

    class Meta:
        model = UserMission
        fields = ("result",)


class UserMissionReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор проверки миссии (для HR/Организатора).
    """

    class Meta:
        model = UserMission
        fields = (
            "status",
            "review_comment",
        )

    def validate_status(self, value):
        """Проверка статуса."""
        if value not in [UserMission.Status.COMPLETED, UserMission.Status.IN_PROGRESS]:
            raise serializers.ValidationError("Недопустимый статус")
        return value
