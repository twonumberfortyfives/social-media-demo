import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


def upload_to(instance, filename):
    # Generate a unique filename using UUID
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return f"profile_pics/{new_filename}"


def get_random_default_photo():
    photo = f"https://robohash.org/{uuid.uuid4()}.png"
    return photo


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.CharField(blank=True, null=True, max_length=255)
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)

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

    def save(self, *args, **kwargs):
        self.full_clean()
        super(User, self).save(*args, **kwargs)
