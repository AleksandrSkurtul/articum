from django.test import TestCase, Client
from articles.models import Article
from django.contrib.auth import get_user_model
from django.test.utils import setup_test_environment


# class UserCase(TestCase):
#     def setUp(self):
#         get_user_model().objects.create(id=1, username='Alex')
#         get_user_model().objects.create(id=1, username='Vlad')
#         get_user_model().objects.create(id=3, username='Sergey')
#
#
# class ArticleTestCase(TestCase):
#     def setUp(self):
#         Article.objects.create(title='Donec posuere metus vitae ipsum.',
#                                body='Vestibulum ante ipsum primis in faucibus orci;',
#                                user_id=1)
#         Article.objects.create(title='What if gfsd ipsum',
#                                body='Testing smth cool ok no, why',
#                                user_id=2)
#         Article.objects.create(title='Creat',
#                                body='Vakaka raw is weather cool',
#                                user_id=1)
#         Article.objects.create(title='Dnothing',
#                                body='Zeevv 123',
#                                user_id=3)


class GlobalSearchTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(id=1, username='Alex')
        cls.article1 = Article.objects.create(title='Title test 1',
                                              body='',
                                              user_id=1)

        cls.article2 = Article.objects.create(title='Title 2',
                                              body='',
                                              user_id=1)

    def setUp(self):
        self.client = Client()

    def test_search_by_query_returns_article_with_query_in_title(self):
        response = self.client.get('/search/?query=test')
        response_json = response.json()

        articles_result = response_json['Articles by title']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(articles_result[0]['id'], self.article1.id)

    def test_search_by_query_returns_no_article_with_query_in_title(self):
        response = self.client.get('/search/?query=something')
        response_json = response.json()

        articles_result = response_json['Articles by title']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(articles_result), 0)
