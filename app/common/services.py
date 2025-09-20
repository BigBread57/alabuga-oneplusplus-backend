from typing import Any


class BaseService:
    """Базовый сервис."""

    @staticmethod
    def set_attrs(obj, validated_data: dict[str, Any]):
        """Установка значений для объекта."""
        for key_item, value_item in validated_data.items():
            setattr(obj, key_item, value_item)
