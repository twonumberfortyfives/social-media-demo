from django.db import models

from user.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=500)
    media = models.ImageField(upload_to="")
    created_at = models.DateTimeField(auto_now_add=True)
    