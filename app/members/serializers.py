from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(ModelActionSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'nickname', 'address', 'gender', ]
        action_fields = {
            'login': {'fields': ('username', 'password')}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
