from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user.views import Register, MyProfile, VerifyEmail

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("register/", Register.as_view(), name="signup"),
    path("my-profile/", MyProfile.as_view(), name="my_profile"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

]

