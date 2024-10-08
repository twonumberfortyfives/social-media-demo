from django.urls import path
from rest_framework import routers

from follow.views import FollowViewSet

router = routers.DefaultRouter()
router.register("follows", FollowViewSet)

urlpatterns = []

urlpatterns += router.urls

app_name = "follow"
