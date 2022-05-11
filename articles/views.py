from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from articles.models import Article
from articles.serializers import ArticleSerializer


class ArticleViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        else:
            return [IsAuthenticatedOrReadOnly()]
