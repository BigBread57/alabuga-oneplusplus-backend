from rest_framework import serializers

from apps.missions.models import MissionBranch


class MissionBranchListSerializer(serializers.ModelSerializer):
    """
    Ветка миссий. Список объектов.
    """

    missions_count = serializers.SerializerMethodField()

    class Meta:
        model = MissionBranch
        fields = (
            "id",
            "name",
            "description",
            "category",
            "icon",
            "order",
            "missions_count",
        )

    def get_missions_count(self, obj):
        """Получить количество миссий в ветке."""
        return obj.missions.filter(is_active=True).count()


class MissionBranchDetailSerializer(serializers.ModelSerializer):
    """
    Ветка миссий. Детальная информация.
    """

    missions = serializers.SerializerMethodField()

    class Meta:
        model = MissionBranch
        fields = (
            "id",
            "name",
            "description",
            "category",
            "icon",
            "order",
            "missions",
            "created_at",
            "updated_at",
        )

    def get_missions(self, obj):
        """Получить миссии ветки."""
        from apps.missions.serializers import MissionListSerializer

        missions = obj.missions.filter(is_active=True)
        return MissionListSerializer(missions, many=True, context=self.context).data
