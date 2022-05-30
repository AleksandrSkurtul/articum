from django.urls import path, include

import articles
from accounts.views import AccountFollow, AccountUnfollow

urlpatterns = [
    path('<username>/follow/', AccountFollow.as_view()),
    path('<username>/unfollow/', AccountUnfollow.as_view()),
]
