from django.conf import settings
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.name} {self.date}'
