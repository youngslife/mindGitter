from rest_framework import serializers
from accounts.models import User


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]
