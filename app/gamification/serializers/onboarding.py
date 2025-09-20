from rest_framework import serializers

from apps.gamification.models import BoardingStep, UserBoardingProgress


class BoardingStepSerializer(serializers.ModelSerializer):
    """
    Шаг онбординга.
    """
    
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = BoardingStep
        fields = (
            "id",
            "title",
            "content",
            "order",
            "is_active",
            "is_completed",
        )
        
    def get_is_completed(self, obj):
        """Проверить, завершен ли шаг пользователем."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserBoardingProgress.objects.filter(
                user=request.user,
                step=obj,
                completed_at__isnull=False
            ).exists()
        return False
        
        
class UserBoardingProgressSerializer(serializers.ModelSerializer):
    """
    Прогресс пользователя в онбординге.
    """
    
    step_title = serializers.CharField(source='step.title', read_only=True)
    
    class Meta:
        model = UserBoardingProgress
        fields = (
            "id",
            "step",
            "step_title",
            "completed_at",
        )
        read_only_fields = ('completed_at',)