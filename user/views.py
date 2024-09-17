import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls.base import reverse
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.serializers import (
    RegisterSerializer,
    MyProfileSerializer,
    EmailVerificationSerializer,
)
from user.utils import Util


class Register(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create a token for the user
        tokens = RefreshToken.for_user(user).access_token

        # Generate the email verification URL
        current_site = get_current_site(request).domain
        relative_link = reverse("user:email-verify")  # Assuming you have an email-verify URL
        absurl = f"http://{current_site}{relative_link}?token={tokens}"
        email_body = (
            f"Hi {user.username}, Use the link below to verify your email:\n{absurl}"
        )

        # Send the email
        email_data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }
        Util.send_email(data=email_data)

        # Return success response
        return Response(
            {
                "message": f"{user.username} registered successfully. Check your {user.email} for verification link.",
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmail(GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(
                token, options={"verify_signature": False}
            )  # decoding the access token getting user id from it
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class MyProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyProfileSerializer

    def get_object(self):
        return self.request.user


def sign_up_view(request):
    return render(request, "sign_up.html")


def sign_in_view(request):
    return render(request, "sign_in.html")
