from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from members.models import UserAddress

User = get_user_model()


class UserAddressCreateSerializers(ModelSerializer):
    class Meta:
        model = UserAddress
        fiedls = ('address',)


class UserAddressSerializers(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'address', 'detail_address', 'require_message', 'status',
                  'recieving_place', 'entrance_password', 'free_pass', 'etc', 'message')


class UserSerializer(ModelActionSerializer):
    address = UserAddressSerializers(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'phone', 'nickname', 'gender', 'address')
        action_fields = {
            'login': {'fields': ('username', 'password')},
            'check_username': {'fields': ('username',)},
            'check_email': {'fields': ('email',)},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        address = self.context['request'].data['address']
        #        UserAddressCreateSerializers(address).is_valid(raise_exception=True)
        UserAddress.objects.create(user=user, address=address, status='T')
        return user
