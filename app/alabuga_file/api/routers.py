from rest_framework.routers import APIRootView
from server.apps.alabuga_file.api.views import AlabugaFileViewSet
from server.apps.services.drf_nova_router.api_router import ApiRouter


class AlabugaFileAPIRootView(APIRootView):
    """Корневой view для апи."""

    __doc__ = "Файлы пользователей"
    name = "alabuga_file"


router = ApiRouter()
router.APIRootView = AlabugaFileAPIRootView

router.register("cicada-files", AlabugaFileViewSet, "cicada-files")
