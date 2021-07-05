from rest_framework import routers
from .api import WebSiteTags, WebSiteCheck, Auth

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'^structure', WebSiteTags, 'website_tags_searching_default')
router.register(r'^check_structure', WebSiteCheck, 'website_check')
router.register(r'^login', Auth, 'website_check')
urlpatterns = router.urls