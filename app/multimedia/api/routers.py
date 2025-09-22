from rest_framework.routers import APIRootView
from server.apps.alabuga_file.api.views import MultimediaViewSet
from server.apps.services.drf_nova_router.api_router import ApiRouter


class MultimediaAPIRootView(APIRootView):
    """Корневой view для апи."""

    __doc__ = "Файлы пользователей"
    name = "alabuga_file"


router = ApiRouter()
router.APIRootView = MultimediaAPIRootView

router.register("cicada-files", MultimediaViewSet, "cicada-files")
