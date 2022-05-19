from django.urls import path, include
from rest_framework import routers

from articles.views import ArticleViewSet, UserArticlesViewSet

router = routers.DefaultRouter()

router.register('articles', ArticleViewSet)

urlpatterns = [
    path('users/<username>/articles/', UserArticlesViewSet.as_view()),
    path('', include(router.urls))
]
