from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from members.models import UserAddress

User = get_user_model()


class UserAddressSerializers(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('id', 'detail_address', 'require_message', 'status', 'recieving',)


class UserSerializer(ModelActionSerializer):
    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'email', 'phone', 'nickname', 'gender',
                  )

        action_fields = {
            'login': {'fields': ('username', 'password')},
            'check_username': {'fields': ('username',)},
            'check_email': {'fields': ('email',)},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
