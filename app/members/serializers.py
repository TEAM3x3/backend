from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'name', 'address', 'gender', 'birthdate']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(ModelActionSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'name', 'address', 'gender', 'birthdate']
        action_fields = {
            'login': {'fields': ('username', 'password')}
        }