from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import Article
from articles.serializers import ArticleSerializer, UserSerializer


class Search(APIView):

    def get(self, request, format=None, **kwargs):
        query = self.request.query_params['query']
        offset = int(self.request.query_params.get('offset', 0))
        limit = int(self.request.query_params.get('limit', 2))

        articles_searched_by_title = Article.objects.filter(title__icontains=query)[
                                     offset:offset + limit]
        articles_searched_by_body = Article.objects.filter(body__icontains=query)[
                                    offset:offset + limit]
        users_searched_by_username = get_user_model().objects.filter(username__icontains=query)[
                                     offset:offset + limit]

        articles_searched_by_title_serializer = ArticleSerializer(articles_searched_by_title, many=True)
        articles_searched_by_body_serializer = ArticleSerializer(articles_searched_by_body, many=True)
        users_searched_by_username_serializer = UserSerializer(users_searched_by_username, many=True)

        return Response(
            {
                "articles_by_title": articles_searched_by_title_serializer.data,
                "users_by_name": users_searched_by_username_serializer.data,
                "articles_by_body": articles_searched_by_body_serializer.data,
            }
        )
