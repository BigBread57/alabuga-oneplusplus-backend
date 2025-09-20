from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer as BaseTokenRefreshSerializer

User = get_user_model()


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    """
    Сериализатор получения JWT токена.
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token


class TokenRefreshSerializer(BaseTokenRefreshSerializer):
    """
    Сериализатор обновления JWT токена.
    """
    pass


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        """Проверка совпадения паролей."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        """Создание пользователя."""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user