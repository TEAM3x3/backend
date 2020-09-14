from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from members.models import UserAddress

User = get_user_model()


class UserAddressCreateSerializers(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('address',)


class UserAddressSerializers(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('id', 'address', 'detail_address', 'require_message', 'status', 'user')

    def create(self, validated_data):
        if validated_data['status'] == 'T':
            for ins in self.Meta.model.objects.filter(user__pk=self.data.get('user')):
                ins.status = 'F'
                ins.save()
        return super().create(validated_data)


    def update(self, instance, validated_data):
        qs = self.Meta.model.objects.all().exclude(pk=instance.pk)
        bulk_list = []
        for ins in self.Meta.model.objects.all().exclude(pk=instance.pk):
            ins.status = 'F'
            bulk_list.append(ins)
            # bulk update
            # ins.save()
        self.Meta.model.objects.bulk_update(bulk_list, ['status'])
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if validated_data['status'] == 'T':
            for ins in UserAddress.objects.filter(user=self.data.get('user')):
                ins.status = 'F'
                ins.save()
        return super().create(validated_data)


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
        user = User.objects.create_user(**validated_data)
        address = self.context['request'].data['address']
        #        UserAddressCreateSerializers(address).is_valid(raise_exception=True)
        UserAddress.objects.create(user=user, address=address, status='T')
        return user
