from django.db import models
from rest_framework.exceptions import ValidationError

from user.models import User


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, null=False, blank=False)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('follower', 'followed'),)

    @staticmethod
    def validate_follow_yourself(following_user, followed_user):
        equal = followed_user == following_user
        return equal

    def clean(self):
        if self.validate_follow_yourself(self.follower, self.followed):
            raise ValidationError('You cannot follow yourself!')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Follow, self).save(*args, **kwargs)
