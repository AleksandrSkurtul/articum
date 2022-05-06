from rest_framework import routers

from articles.views import ArticleViewSet

router = routers.DefaultRouter()

router.register('', ArticleViewSet, basename='articles')

urlpatterns = router.urls
