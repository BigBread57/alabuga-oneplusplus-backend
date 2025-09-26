from typing import TypeVar

from django.db.models import QuerySet
from django_filters import FilterSet

T = TypeVar("T")


class CurrentCharacterDefault:
    """
    Возвращает персонажа текущего пользователя по умолчанию.
    """

    requires_context = True

    def __call__(self, serializer_field):
        user = serializer_field.context["request"].user
        if hasattr(user, "character"):
            return user.character
        return None


class BaseSelector:
    """
    Класс, который позволяет формировать корректный селектор.
    """

    queryset: QuerySet[T]
    filter_class: type[FilterSet] | None = None

    def __init__(self, request=None):
        self.request = request

    def get_queryset(self, **kwargs) -> QuerySet[T]:
        """
        Получить queryset.
        """
        assert self.queryset is not None, "Attribute queryset is required."
        return self.queryset

    def get_filter_class(self) -> type[FilterSet]:
        """
        Получить класс, который отвечает за фильтры queryset.
        """
        return self.filter_class

    def get_filtered(self, queryset: QuerySet[T], filters: dict | None = None) -> QuerySet[T]:
        """
        Получить отфильтрованный queryset.
        """
        if self.filter_class:
            return self.get_filter_class()(filters, queryset=queryset).qs

        return self.get_queryset()
