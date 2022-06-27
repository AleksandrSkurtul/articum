from django.test import TestCase, Client
from articles.models import Article
from accounts.models import UserAccount
from django.contrib.auth import get_user_model


class GlobalSearchTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # create users
        get_user_model().objects.create(id=1, username='Alex')
        get_user_model().objects.create(id=2, username='Bob')
        get_user_model().objects.create(id=3, username='John')
        get_user_model().objects.create(id=4, username='Vlad')
        get_user_model().objects.create(id=5, username='Carl')

        # create accounts
        cls.user1 = UserAccount.objects.create(user_id=1)
        cls.user2 = UserAccount.objects.create(user_id=2)
        cls.user3 = UserAccount.objects.create(user_id=3)
        cls.user4 = UserAccount.objects.create(user_id=4)
        cls.user5 = UserAccount.objects.create(user_id=5)

        # create articles
        cls.article1 = Article.objects.create(title='One',
                                              body='Some text in first article',
                                              user_id=1)

        cls.article2 = Article.objects.create(title='Two',
                                              body='More text in second article',
                                              user_id=1)

        cls.article2 = Article.objects.create(title='Three',
                                              body='Something',
                                              user_id=2)

        cls.article2 = Article.objects.create(title='Four',
                                              body='',
                                              user_id=3)

        # add likes
        cls.user1.liked_articles.set([cls.article1, cls.article2])

    def setUp(self):
        self.client = Client()

    def test_search_by_query_returns_one_article_by_title(self):
        response = self.client.get('/search/?query=one')
        response_json = response.json()

        articles_by_title_result = response_json['Articles by title']
        articles_by_body_result = response_json['Articles by body']
        users_by_username_result = response_json['Users by name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(articles_by_title_result), 1)
        self.assertEqual(len(articles_by_body_result), 0)
        self.assertEqual(len(users_by_username_result), 0)

    def test_search_by_query_returns_one_article_by_body(self):
        response = self.client.get('/search/?query=second')
        response_json = response.json()

        articles_by_title_result = response_json['Articles by title']
        articles_by_body_result = response_json['Articles by body']
        users_by_username_result = response_json['Users by name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(articles_by_title_result), 0)
        self.assertEqual(len(articles_by_body_result), 1)
        self.assertEqual(len(users_by_username_result), 0)

    def test_search_by_query_returns_one_user_by_name(self):
        response = self.client.get('/search/?query=alex')
        response_json = response.json()

        articles_by_title_result = response_json['Articles by title']
        articles_by_body_result = response_json['Articles by body']
        users_by_username_result = response_json['Users by name']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(articles_by_title_result), 0)
        self.assertEqual(len(articles_by_body_result), 0)
        self.assertEqual(len(users_by_username_result), 1)

    def test_search_by_query_returns_nothing(self):
        response = self.client.get('/search/?query=nothing')
        response_content = response.content

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response_content,
            {'Articles by title': [],
             'Users by name': [],
             'Articles by body': []
             }
        )
