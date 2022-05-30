from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model

from accounts.models import UserAccount
from articles.models import Article, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name']


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    likes_count = serializers.SerializerMethodField(method_name='get_likes_count')

    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'likes_count', 'user', ]

    def get_likes_count(self, instance):
        return instance.likes.count()


class CreateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'body']

    def create(self, validated_data):
        user_id = self.context.get('user_id', None)
        article = Article.objects.create(user_id=user_id, **validated_data)
        return article


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article_id', 'user_id', 'message', 'date']


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message']

    def create(self, validated_data):
        user_id = self.context.get('user_id', None)
        article_id = self.context.get('article_id', None)
        comment = Comment.objects.create(user_id=user_id, article_id=article_id, **validated_data)
        return comment
