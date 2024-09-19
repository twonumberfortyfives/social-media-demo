import os
import shutil
import uuid
import requests

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from rest_framework_simplejwt.tokens import RefreshToken


def image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"

    return os.path.join("profile_pics/", filename)


def get_random_default_photo():
    photo = f"https://robohash.org/{uuid.uuid4()}"
    file_name = f"media/profile_pics/{uuid.uuid4()}"
    response = requests.get(photo, stream=True)
    if response.status_code == 200:
        with open(file_name + ".png", "wb") as f:
            shutil.copyfileobj(response.raw, f)
    else:
        return None
    return file_name[6:] + ".png"


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.CharField(blank=True, null=True, max_length=255)
    profile_picture = models.ImageField(upload_to=image_file_path, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def clean(self):
        if not self.profile_picture:
            self.profile_picture = get_random_default_photo()
        if not self.bio:
            self.bio = "nothing."

    def save(self, *args, **kwargs):
        self.full_clean()
        super(User, self).save(*args, **kwargs)
