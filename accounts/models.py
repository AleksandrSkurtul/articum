from django.db import models
from articles.models import Article


class UserAccount(models.Model):
    user = models.OneToOneField('auth.User', null=False, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    liked_articles = models.ManyToManyField(Article)

    def follow(self, account):
        self.follows.add(account)

    def unfollow(self, account):
        self.follows.remove(account)

    def like(self, article):
        self.liked_articles.add(article)

    def unlike(self, article):
        self.liked_articles.remove(article)
