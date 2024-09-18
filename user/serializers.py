from rest_framework import serializers

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_verified",
            "tokens",
            "profile_picture",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        read_only_fields = ("id", "is_verified")

    def create(self, validated_data):
        password = validated_data["password"]
        if password:
            user = User.objects.create_user(
                username=validated_data["username"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                email=validated_data["email"],
                profile_picture=validated_data["profile_picture"],
            )
            user.set_password(password)
            user.save()
            return user


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "is_verified",
            "bio",
            "profile_picture",
        )
        read_only_fields = ("id", "is_verified")


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]
