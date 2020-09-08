from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserAddressSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'address', 'detail_address', 'require_message', 'status', 'recieving',)


class UserSerializer(ModelActionSerializer):
    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'email', 'phone', 'nickname', 'address', 'gender',
                  # 'birthday'
                  )

        action_fields = {
            'login': {'fields': ('username', 'password')},
            'check_username': {'fields': ('username',)},
            'check_email': {'fields': ('email',)},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

