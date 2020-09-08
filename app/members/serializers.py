from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from members.models import UserAddress

User = get_user_model()


class UserAddressSerializers(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('id', 'address', 'detail_address', 'require_message', 'status')


class UserSerializer(ModelActionSerializer):
    address = UserAddressSerializers(read_only=True, many=True)

    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'email', 'phone', 'nickname', 'gender', 'address')

        action_fields = {
            'login': {'fields': ('username', 'password')},
            'check_username': {'fields': ('username',)},
            'check_email': {'fields': ('email',)},
        }

    def create(self, validated_data):
        address = validated_data.pop('context')
        user = User.objects.create_user(**validated_data)
        UserAddress.objects.create(user=user, address=address, status='T')
        return user
