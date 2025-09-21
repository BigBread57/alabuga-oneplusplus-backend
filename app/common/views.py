from types import FunctionType
from typing import Any, Optional, TypeVar

from rest_framework.fields import MultipleChoiceField
from rest_framework.relations import ManyRelatedField
from rest_framework.serializers import ListSerializer, Serializer

from apps.common.selectors import BaseSelector

T = TypeVar("T")


class QuerySelectorMixin:
    """Класс позволяет получить queryset в представлениях из селектора."""

    selector: BaseSelector
    filter_params_serializer_class: Optional[type[Serializer]] = None

    def get_queryset(self, **kwargs) -> T:
        """Получить queryset из селектора."""
        assert self.selector is not None, "Attribute selector must be set."
        if isinstance(self.selector, FunctionType):
            return self.selector()
        return self.selector().get_queryset(**kwargs)

    def get_filter_params_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Корректно преобразовать данные для фильтра в словарь."""
        fields = self.filter_params_serializer_class.get_fields(self.filter_params_serializer_class)
        for query_param_name, query_param_value in self.request.query_params.items():
            if isinstance(fields.get(query_param_name), ManyRelatedField | ListSerializer | MultipleChoiceField):
                data.update({query_param_name: self.request.query_params.getlist(query_param_name)})
            else:
                data.update({query_param_name: query_param_value})
        return data

    def filter_queryset(self, queryset: T) -> T:
        """Получить отфильтрованный queryset из селектора."""
        if self.filter_params_serializer_class:
            context = self.get_serializer_context()
            data = {**self.kwargs}
            filter_serializer = self.filter_params_serializer_class(
                data=self.get_filter_params_data(data=data),
                context=context,
            )
            filter_serializer.is_valid(raise_exception=True)
            if isinstance(self.selector, FunctionType):
                queryset = self.selector(filters=filter_serializer.validated_data)
            else:
                queryset = self.selector().get_filtered(
                    queryset=queryset,
                    filters=filter_serializer.validated_data,
                )
        return queryset

    @classmethod
    def as_view(cls, **kwargs):
        if hasattr(cls, "selector") and isinstance(cls.selector, FunctionType):
            cls.selector = staticmethod(cls.selector)

        return super().as_view(**kwargs)
