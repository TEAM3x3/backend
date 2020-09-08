from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
<<<<<<< HEAD
=======

from members.models import UserAddress
>>>>>>> aac0997f205ffeac4d97c8d453b3b32fde671294

User = get_user_model()


class UserAddressSerializers(ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = User
=======
        model = UserAddress
>>>>>>> aac0997f205ffeac4d97c8d453b3b32fde671294
        fields = ('id', 'address', 'detail_address', 'require_message', 'status', 'recieving',)


class UserSerializer(ModelActionSerializer):
    # address = UserAddressSerializers()

    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'email', 'phone', 'nickname', 'gender')

        action_fields = {
            'login': {'fields': ('username', 'password')},
            'check_username': {'fields': ('username',)},
            'check_email': {'fields': ('email',)},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

