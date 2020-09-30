from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from members.models import UserAddress, UserSearch, KeyWord

User = get_user_model()


class UserAddressSerializers(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAddress
        fields = ('id', 'address', 'detail_address', 'status', 'user')
        examples = {
            'address': '성수동',
            'detail_address': "제강빌딩",
            'status': 'T',
        }

    def update(self, instance, validated_data):
        qs = self.Meta.model.objects.all().exclude(id=instance.id)
        bulk_list = []
        for ins in self.Meta.model.objects.all().exclude(id=instance.id):
            ins.status = 'F'
            bulk_list.append(ins)

        self.Meta.model.objects.bulk_update(bulk_list, ['status'])
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if validated_data['status'] == 'T':
            for ins in UserAddress.objects.filter(user=validated_data['user']):
                ins.status = 'F'
                ins.save()
        return super().create(validated_data)


class UserOrderAddressSerializers(ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAddress
        fields = (
            'id', 'address', 'detail_address', 'status', 'receiving_place', 'entrance_password', 'free_pass', 'etc',
            'message', 'extra_message', 'user',)
        examples = {
            'id': 1,
            "address": "아파트 까지의 정보만 저장할 예정입니다.",
            "detail_address": "동 호수에 대한 정보입니다.",
            "status": "T",
            "receiving_place": "택배함",
            "entrance_password": "1234",
            "extra_message": "경비실 특이사항, 택배함 정보 데이터, 기타 장소 세부사항에 대한 값을 저장합니다. receiving_place에 대한 값에 종속성을 가집니다."
        }

    def update(self, instance, validated_data):
        bulk_list = []
        for ins in self.Meta.model.objects.all().exclude(id=instance.id):
            ins.status = 'F'
            bulk_list.append(ins)
        self.Meta.model.objects.bulk_update(bulk_list, ['status'])
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if validated_data['status'] == 'T':
            for ins in UserAddress.objects.filter(user=validated_data['user']):
                ins.status = 'F'
                ins.save()
        return super().create(validated_data)


class UserSerializer(ModelActionSerializer):
    address = UserAddressSerializers(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'phone', 'nickname', 'gender', 'address',)
        examples = {
            "username": "test_user1111",
            "password": "1111",
            "email": "test_user1111@email.com",
            "phone": "010-1111-1111",
            "gender": "N",
            "address": "서울시 성동구"
        }
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
