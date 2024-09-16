from rest_framework import generics

from user.models import User
from user.serializers import RegisterSerializer, MyProfileSerializer


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class MyProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyProfileSerializer

    def get_object(self):
        return self.request.user
