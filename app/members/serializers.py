from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from members.models import UserAddress, UserSearch, KeyWord

User = get_user_model()


class UserAddressSerializers(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('id', 'address', 'detail_address', 'require_message', 'user', 'status')

    def create(self, validated_data):
        if validated_data['status'] == 'T':
            for ins in self.Meta.model.objects.filter(user__id=self.data.get('user')):
                ins.status = 'F'
                ins.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        qs = self.Meta.model.objects.all().exclude(id=instance.id)
        bulk_list = []
        for ins in self.Meta.model.objects.all().exclude(id=instance.id):
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

        fields = ('id', 'username', 'password', 'email', 'phone', 'nickname', 'gender', 'address',)

        action_fields = {
            'login': {'fields': ('username', 'password',)},
            'check_username': {'fields': ('username',)},
            'check_email': {'fields': ('email',)},
            'find_id': {'fields': ('nickname', 'email', 'username',)},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        address = self.context['request'].data['address']
        #        UserAddressCreateSerializers(address).is_valid(raise_exception=True)
        UserAddress.objects.create(user=user, address=address, status='T')
        return user


class UserSearchSerializer(ModelActionSerializer):
    # keyword = serializers.StringRelatedField()

    class Meta:
        model = UserSearch
        fields = ('id', 'user', 'keyword',)
        validators = [
            UniqueTogetherValidator(
                queryset=UserSearch.objects.all(),
                fields=['user', 'keyword']
            )
        ]


class PopularSerializer(ModelActionSerializer):
    class Meta:
        model = KeyWord
        fields = ('id', 'name', 'count')


class UserOrderSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
