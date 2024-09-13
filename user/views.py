from rest_framework import viewsets, generics

from user.models import User
from user.serializers import RegisterSerializer


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
