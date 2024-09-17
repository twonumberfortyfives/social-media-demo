from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import Register, MyProfile, VerifyEmail, sign_up_view, sign_in_view

urlpatterns = [
    path("api_v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api_v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api_v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api_v1/register/", Register.as_view(), name="register"),
    path("api_v1/my-profile/", MyProfile.as_view(), name="my_profile"),
    path("api_v1/email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("sign-up/", sign_up_view, name="sign-up"),
    path("sign-in/", sign_in_view, name="sign-in"),
]

app_name = "user"