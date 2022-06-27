from django.test import TestCase, Client
from articles.models import Article
from django.contrib.auth import get_user_model


class GlobalSearchTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(id=1, username='Alex')
        cls.article1 = Article.objects.create(title='First Article',
                                              body='Some text in body',
                                              user_id=1)

        cls.article2 = Article.objects.create(title='Second Article',
                                              body='More text in body',
                                              user_id=1)

    def setUp(self):
        self.client = Client()

    def test_search_by_query_returns_article_with_query_in_title(self):
        response = self.client.get('/search/?query=first')
        response_json = response.json()

        articles_result = response_json['Articles by title']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(articles_result[0]['id'], self.article1.id)

    def test_search_by_query_returns_nothing(self):
        response = self.client.get('/search/?query=nothing')
        response_json = response.json()

        articles_result = response_json['Articles by title', 'Articles by body', 'Users by name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(articles_result), 0)
