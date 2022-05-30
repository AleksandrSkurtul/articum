from django.urls import path, include
from rest_framework_nested import routers

from articles.views import ArticleViewSet, UserArticlesViewSet, LikeArticle, CommentViewSet

router = routers.DefaultRouter()

router.register('articles', ArticleViewSet)

articles_router = routers.NestedSimpleRouter(router, 'articles')
articles_router.register('comments', CommentViewSet)

urlpatterns = [
    path('users/<username>/articles/', UserArticlesViewSet.as_view()),
    path('articles/<article_id>/like', LikeArticle.as_view()),
    path('', include(router.urls)),
    path('', include(articles_router.urls))
]
