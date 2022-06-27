from django.db.models import Count
from rest_framework import status
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter

from accounts.models import UserAccount
from articles.models import Article, Comment
from articles.pagination import DefaultPagination
from articles.serializers import ArticleSerializer, CreateArticleSerializer, CommentSerializer, \
    CreateCommentSerializer


class ArticleViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']
    queryset = Article.objects.annotate(likes_count=Count('likes')).order_by('likes_count').reverse()
    filter_backends = [SearchFilter]
    search_fields = ['title', 'body', 'user__username']
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return CreateArticleSerializer
        else:
            return ArticleSerializer

    def create(self, request):
        serializer = CreateArticleSerializer(
            data=request.data,
            context={'user_id': self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        article = self.get_object()
        if article.user_id == self.request.user.id:
            serializer = CreateArticleSerializer(
                data=request.data,
                context={'user_id': self.request.user.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.update(article, serializer.data)
            return Response(serializer.data)
        return Response({'error': 'You have no permission!'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        if article.user_id != self.request.user.id:
            return Response({'error': 'You have no permission!'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)


class UserArticlesViewSet(ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.select_related('user').filter(
            user__username=self.kwargs.get('username'))


class LikeArticle(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        article_id = kwargs.get("article_id")

        user = UserAccount.objects.prefetch_related('liked_articles').get(user_id=user_id)

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFound("Article with such id doesn't exist!")

        if user.liked_articles.all().filter(id=article_id).exists():
            user.unlike(article)
            return Response(f'Now you unlike {article}', status=status.HTTP_201_CREATED)

        user.like(article)

        return Response(f'Now you like {article}', status=status.HTTP_201_CREATED)


class CommentViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        return Comment.objects.filter(
            article_id=self.kwargs.get('nested_1_pk'))

    def create(self, request, *args, **kwargs):
        serializer = CreateCommentSerializer(
            data=request.data,
            context={
                'user_id': self.request.user.id,
                'article_id': self.kwargs.get('nested_1_pk')
            }
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user_id == self.request.user.id:
            serializer = CreateCommentSerializer(
                data=request.data,
                context={'user_id': self.request.user.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.update(comment, serializer.data)
            return Response(serializer.data)
        return Response({'error': 'You have no permission!'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user_id != self.request.user.id:
            return Response({'error': 'You have no permission!'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
