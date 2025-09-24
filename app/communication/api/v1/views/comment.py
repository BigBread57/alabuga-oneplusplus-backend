import django_filters
from rest_framework.generics import GenericAPIView


class CommentFilter(
    UserFilterMixin,
    CreatedUpdatedDateFilterMixin,
    django_filters.FilterSet,
):
    """Фильтр отзывов."""

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "user_email",
            "user_username",
            "user_first_name",
            "user_last_name",
            "user_middle_name",
            "content_type",
            "object_id",
        )


class CommentListViewSet(GenericAPIView):
    """
    Комментарий. Список.
    """

    serializer_class = CommentSerializer
    create_serializer_class = CreateCommentSerializer
    queryset = Comment.objects.select_related("user")
    search_fields = ("text",)
    ordering_fields = "__all__"
    filterset_class = CommentFilter

    def perform_create(self, serializer):
        """
        Добавляем информацию о пользователе.
        """
        serializer.validated_data.update(user=self.request.user)
        serializer.save()
