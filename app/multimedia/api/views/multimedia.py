import django_filters
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.decorators import action
from server.apps.alabuga_file.api.serialziers import (
    CreateMultimediaSerializer,
    MultimediaSerializer,
)
from server.apps.alabuga_file.models import Multimedia
from server.apps.alabuga_file.services.check_signature import check_signature
from server.apps.services.filters_mixins import CreatedUpdatedDateFilterMixin
from server.apps.services.views import BaseModelViewSet


class MultimediaFilter(
    CreatedUpdatedDateFilterMixin,
    django_filters.FilterSet,
):
    """Фильтр файлов."""

    class Meta:
        model = Multimedia
        fields = (
            "id",
            "object_id",
            "content_type",
            "start_created_at",
            "end_created_at",
            "start_updated_at",
            "end_updated_at",
            "range_created_at",
            "range_updated_at",
        )


class MultimediaViewSet(BaseModelViewSet):
    """Файл. Просмотр, добавление, изменение, удаление.

    Описание: стандартный набор действий для взаимодействия с объектом.

    Доступно: в рамках ролевой модели.
    """

    serializer_class = MultimediaSerializer
    create_serializer_class = CreateMultimediaSerializer
    queryset = Multimedia.objects.select_related("creator", "content_type")
    ordering_fields = "__all__"
    filterset_class = MultimediaFilter
    permission_type_map = {
        **BaseModelViewSet.permission_type_map,  # type: ignore
        "check_permission": None,
    }

    def get_queryset(self):
        """Выдача файлов.

        Суперпользователь видит все файлы.
        Остальные видят файлы, в рамках своих компаний.
        """
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return queryset

        return queryset.filter(
            company__in=user.companies.all(),
        )

    @action(
        methods=["GET"],
        url_path="check-permission",
        detail=False,
        authentication_classes=[
            SessionAuthentication,
            BasicAuthentication,
            TokenAuthentication,
        ],
        permission_classes=[permissions.AllowAny],
    )
    def check_permission(self, request):
        """Проверка для хранилища, что пользователь авторизован.

        На данную api пересылаются все запросы, которые летят в minio.
        Сделано это для проверки авторизации пользователя, который совершает
        запрос. Если пользователь авторизован, то мы предоставляем доступ к
        файлам.
        """
        # Если пользователь авторизован в системе (при GET запросах),
        # то разрешаем получить файл.
        if request.user.is_authenticated:
            return HttpResponse(status=status.HTTP_200_OK)

        # В случае PUT запросов (когда добавляется файл через api или админку)
        # Запрос на данную api приходит без данных о пользователе, поэтому мы
        # анализируем заголовки, которые подставляет boto3.
        if check_signature(request=request):
            return HttpResponse(status=status.HTTP_200_OK)

        # В остальных случаях запрещаем доступ к файлам.
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
