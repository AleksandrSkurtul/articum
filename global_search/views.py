from django.contrib.auth import get_user_model
from articles.models import Article
from articles.serializers import ArticleSerializer, UserSerializer
from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 2


class Search(ObjectMultipleModelAPIView):
    pagination_class = LimitPagination

    def get_querylist(self):
        query = self.request.query_params['query']

        users_searched_by_username = get_user_model().objects.filter(username__icontains=query)

        articles_searched_by_title = Article.objects.filter(title__icontains=query)
        articles_searched_by_body = Article.objects.filter(body__icontains=query)

        articles_searched_result = articles_searched_by_title.union(articles_searched_by_body)

        querylist = [
            {
                'queryset': articles_searched_result,
                'serializer_class': ArticleSerializer,
            },
            {
                'queryset': users_searched_by_username,
                'serializer_class': UserSerializer,
            },
        ]

        return querylist
