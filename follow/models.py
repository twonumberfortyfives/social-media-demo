from django.db import models

from user.models import User


class Follow(models.Model):
    following_user_id = models.ManyToManyField(User, related_name='followers_following')
    followed_user_id = models.ManyToManyField(User, related_name='followers_followed')
    created_at = models.DateTimeField(auto_now_add=True)
