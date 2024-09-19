from rest_framework import serializers

from follow.models import Follow


class FollowListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ("id", "follower", "followed", "created_at")

    def validate(self, data):
        common = Follow.validate_follow_yourself(data["follower"], data["followed"])
        if common:
            raise serializers.ValidationError("You can not follow yourself.")
        return data
