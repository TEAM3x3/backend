from action_serializer import ModelActionSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, raise_errors_on_nested_writes
from rest_framework.utils import model_meta
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
            'login': {'fields': ('id', 'username', 'email', 'phone', 'nickname', 'gender', 'address')},
            'check_username': {'fields': ('username',)},
            'check_email': {'fields': ('email',)},
            'find_id': {'fields': ('nickname', 'email', 'username',)},
        }
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        address = self.context['request'].data['address']
        UserAddress.objects.create(user=user, address=address, status='T')
        return user


class UserUpdateSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'nickname', 'email', 'phone', 'gender', 'birthday',)
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)

        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        m2m_fields = []

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        if password:
            instance.set_password(self.validated_data.get('password'))

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class KeywordSerializers(ModelSerializer):
    class Meta:
        model = KeyWord
        fields = ('id', 'name', 'count', 'updated_at')


class UserSearchSerializer(ModelActionSerializer):
    class Meta:
        model = UserSearch
        fields = ('id', 'user', 'keyword',)
        validators = [
            UniqueTogetherValidator(
                queryset=UserSearch.objects.all(),
                fields=['user', 'keyword']
            )
        ]


class UserSearchListSerializer(ModelActionSerializer):
    keyword = KeywordSerializers()

    class Meta:
        model = UserSearch
        fields = ('id', 'user', 'keyword',)
        examples = [
            {
                "id": 2,
                "user": 1,
                "keyword": {
                    "id": 2,
                    "name": "강아지",
                    "count": 1,
                    "updated_at": "2020-10-01"
                }
            },
            {
                "id": 1,
                "user": 1,
                "keyword": {
                    "id": 1,
                    "name": "간식",
                    "count": 2,
                    "updated_at": "2020-10-01"
                }
            }
        ]


class PopularSerializer(ModelActionSerializer):
    class Meta:
        model = KeyWord
        fields = ('id', 'name', 'count')


class UserOrderSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

# class AuthPhoneNumSerializer(ModelSerializer):
#     class Meta:
#         model = AuthPhoneNum
#         fields = (
#             'id',
#             'phone_number',
#             'auth_number',
#             'registration_id',
#         )
#
#         read_only_fields = ('auth_number',)
#
#     def validate_registration_id(self, attrs):
#         if not len(attrs) == 7:
#             raise serializers.ValidationError('생년월일을 입력해주세요.')
#
#         if attrs[-1:] in ['1', '2']:
#             birth = date(int(f'19{attrs[0:2]}'), int(attrs[2:4]), int(attrs[4:6]))
#             year = (date.today() - birth).days / 365
#
#             if year >= 23:
#                 return attrs
#             else:
#                 raise serializers.ValidationError('23세 이하는 가입할수 없습니다.')
#
#         elif attrs[-1:] in ['3', '4']:
#             birth = date(int(f'20{attrs[0:2]}'), int(attrs[2:4]), int(attrs[4:6]))
#             year = (date.today() - birth).days / 365
#
#             if year >= 23:
#                 return attrs
#             else:
#                 raise serializers.ValidationError('23세 이하는 가입할수 없습니다.')
#
#
# class CheckAuthNumberSerializer(ModelSerializer):
#     check_auth_number = serializers.IntegerField(write_only=True)
#
#     class Meta:
#         model = AuthPhoneNum
#         fields = (
#             'id',
#             'check_auth_number',
#         )
#
#         read_only_fields = ('auth_number',)
#
#     def validate_check_auth_number(self, attrs):
#         if len(str(attrs)) == 6:
#             return attrs
#         else:
#             raise serializers.ValidationError('6자리를 입력해주세요.')
