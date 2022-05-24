from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

from accounts.models import UserAccount


class AccountFollow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        followee_username = kwargs.get("username")
        follower_id = self.request.user.id

        try:
            followee = UserAccount.objects.get(user__username=followee_username)
        except UserAccount.DoesNotExist:
            raise NotFound("Account with such name doesn't exist!")

        follower = UserAccount.objects.get(user_id=follower_id)
        if follower == followee:
            raise APIException("You can't follow yourself!")

        follower.follow(followee)

        return Response(f'Now you follow {followee_username}', status=status.HTTP_201_CREATED)


class AccountUnfollow(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        followee_username = kwargs.get("username")
        follower_id = self.request.user.id

        try:
            followee = UserAccount.objects.get(user__username=followee_username)
        except UserAccount.DoesNotExist:
            raise NotFound("Account with such name doesn't exist!")

        if not UserAccount.objects.filter(user_id=follower_id).filter(
                follows__user__username=followee_username).exists():
            raise APIException("You don't follow this user to unfollow!")

        follower = UserAccount.objects.get(follower_id)
        follower.unfollow(followee)

        return Response(f'Now you unfollow {followee_username}', status=status.HTTP_201_CREATED)
