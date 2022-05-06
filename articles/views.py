from rest_framework.viewsets import ModelViewSet

from articles.models import Article
from articles.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
