from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.accounts.models import UserRole

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка пользователей.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "experience",
            "mana",
            "created_at",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор детальной информации о пользователе.
    """

    current_rank = serializers.SerializerMethodField()
    competencies = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "experience",
            "mana",
            "avatar",
            "current_rank",
            "competencies",
            "is_hr",
            "is_organizer",
            "created_at",
            "updated_at",
        )

    def get_current_rank(self, obj):
        """Получить текущий ранг пользователя."""
        if hasattr(obj, "user_rank"):
            return {
                "id": obj.user_rank.rank.id,
                "name": obj.user_rank.rank.name,
                "order": obj.user_rank.rank.order,
            }
        return None

    def get_competencies(self, obj):
        """Получить компетенции пользователя."""
        return [
            {
                "id": uc.competency.id,
                "name": uc.competency.name,
                "level": uc.level,
            }
            for uc in obj.competencies.select_related("competency")
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления пользователя.
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "avatar",
        )


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор обновления роли пользователя (для HR).
    """

    role = serializers.ChoiceField(choices=UserRole.choices)

    class Meta:
        model = User
        fields = ("role",)
