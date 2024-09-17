from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from follow.models import Follow
from follow.serializers import FollowListSerializer


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer
