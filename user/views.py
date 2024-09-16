import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.urls.base import reverse
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.serializers import RegisterSerializer, MyProfileSerializer, EmailVerificationSerializer
from user.utils import Util


class Register(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        # getting tokens
        user_email = User.objects.get(email=user['email'])
        tokens = RefreshToken.for_user(user_email).access_token
        # send email for user verification
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://' + current_site + relative_link + "?token=" + str(tokens)
        email_body = 'Hi ' + user['username'] + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user['email'],
                'email_subject': 'Verify your email'}

        Util.send_email(data=data)

        return Response({'user_data': user, 'access_token': str(tokens)}, status=status.HTTP_201_CREATED)


class VerifyEmail(GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = self.request.user.tokens()['access']
        print(token)
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            print(payload)
            user = User.objects.get(id=self.request.user.id)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class MyProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyProfileSerializer

    def get_object(self):
        return self.request.user
