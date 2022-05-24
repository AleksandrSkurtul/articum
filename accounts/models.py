from django.db import models


class UserAccount(models.Model):
    user = models.OneToOneField('auth.User', null=False, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

    def follow(self, account):
        self.follows.add(account)

    def unfollow(self, account):
        self.follows.remove(account)
