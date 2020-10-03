from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from members.instructors import MyAutoSchema
from members.models import UserAddress, UserSearch, KeyWord
from members.serializers import UserSerializer, UserAddressSerializers, UserSearchSerializer, PopularSerializer, \
    UserOrderAddressSerializers, UserSearchListSerializer, UserUpdateSerializers
from members.permissions import UserInfoOwnerOrReadOnly
from carts.models import CartItem
from carts.serializers import CartItemSerializer

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserInfoOwnerOrReadOnly,)
    swagger_schema = MyAutoSchema

    def get_permissions(self):
        if self.action in ['user_info', ]:
            return [UserInfoOwnerOrReadOnly()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['partial_update']:
            return UserUpdateSerializers
        return self.serializer_class

    @action(detail=False)
    def check_username(self, request):
        """
        유저 아이디 중복검사

        ----
        Params >>  username 데이터가 필요합니다.

        예제 >> http://13.209.33.72/api/users/check_username?username=admin

        get 요청 시, 중복의 경우 400_BAD_REQUEST / 중복이 아닌 경우 200_OK 가 리턴됩니다.
        """
        username = request.query_params.get('username')
        user = User.objects.filter(username=username)
        if user:
            return Response({"message": "이미 사용중인 ID입니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "사용가능한 ID입니다."}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        회원가입

        ---

        ```
        # 요청 json data 예제
        {
            "username":"createUser1",
            "password":"1111",
            "email":"testUser1@user.com",
            "phone":"1112223333",
            "nickname":"관리지",
            "address": "서울시 성동구"

        }

        # 응답 예시 status  201 created
        {
            "id": 4,
            "username": "createUser2",
            "email": "testUser2@user.com",
            "phone": "1112223333",
            "nickname": "관리지",
            "gender": "N",
            "address": [
                {
                    "id": 7,
                    "address": "서울시 성동구",
                    "detail_address": "",
                    "status": "T"
                }
            ]
        }
        ```
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        사용하지 않습니다.

        -----
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        사용자 업데이트

        ----
        - REQUEST BODY SCHEMA 에 나열되어 있는 필드 1개부터 전체 다 보내셔도 됩니다.

        ```

        # 성공 status 200

        {
            "username": "createUser2",
            "nickname": "업데이트",
            "email": "testUser2@user.com",
            "phone": "1112223333",
            "gender": "N",
            "birthday": null
        }
        ```

        """
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        로그인

        ---
        # request examples

        ```
        {
                "username" : "admin",
                "password" : "1111"
        }
        ```

        # response examples
        #### 올바른 요청으로 로그인 시 201_created와 token이 생성됩니다.
        ```
        {
            "token": "88f0566e6db5ebaa0e46eae16f5a092610f46345",
            "user": {
                "username": "admin",
                "email": "rs@rs.com",
                "phone": "000-1111-2222",
                "nickname": "nickname",
                "gender": "N"
            }
        }
        ```

        """
        user = User.objects.get(username=request.data.get('username'))
        serializers = self.get_serializer(user)
        if user.check_password(request.data.get('password')):
            token, __ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "user": serializers.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        """
        로그아웃

        ----
        curl --location --request DELETE 'http://13.209.33.72/api/users/logout' \
        --header 'Authorization: token f979ebb6dc5aaf7af73474c33bd5f087b57cfc4b'
        해당 요청에 토큰을 담아서 보내주세요
        """
        user = request.user
        user.auth_token.delete()
        return Response({"clear"}, status=status.HTTP_200_OK)

    @action(detail=False)
    def user_info(self, request, *args, **kwargs):
        """
        개인정보 수정 API

        -----
        username 과 password 필요.

        {
            "username" : "admin",
            "password" : "1111"
        }
        """
        user = User.objects.get(username=request.user.username)
        if user.check_password(request.data.get('password')):
            profile = User.objects.filter(username=user.username)
            serializer = UserSerializer(profile, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'])
    def password_change(self, request):
        """
        비밀번호 변경 API

        -----
        username 과 password  요청
        """
        user = User.objects.get(username=request.user.username)
        user.set_password(request.data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False)
    def writable(self, request):
        """
        마이컬리 - 상품 후기 - 작성 가능 후기 API

        ----
        헤더에 토큰이 담기지 않으면 에러가 발생합니다.

        작성 가능한 후기들이 카트 아이템의 형태로 나옵니다.
        """
        qs = CartItem.objects.filter(order__user=request.user).filter(status='c')
        serializers = CartItemSerializer(qs, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def find_id(self, request, *args, **kwargs):
        """
        아이디 찾기

        -----
        params >> nickname , email

        예제 http://13.209.33.72/api/users/find_id?nickname=nickname&email=rs@rs.com
        """
        nickname = request.query_params.get('nickname')
        email = request.query_params.get('email')
        user_qs = User.objects.filter(nickname=nickname, email=email)
        serializer = self.serializer_class(user_qs, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAddressViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializers
    swagger_schema = MyAutoSchema  # 추가

    def get_queryset(self):
        try:
            if self.kwargs['user_pk']:
                return self.queryset.filter(user_id=self.kwargs['user_pk'])
        except KeyError:
            return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['order', 'list', 'retrieve', 'partial_update']:
            return UserOrderAddressSerializers
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        {user_pk}가 가진 address list api

        `http://13.209.33.72/api/users/{user_pk}/address` get

        ---
        토큰이 필요하지 않습니다.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        address create

        `http://13.209.33.72/api/users/{user_pk}/address` post
        ----
        해당 요청은 토큰이 필요합니다.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        주소 상제 요청 api

        ----
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        해당 요청은 사용하지 않습니다.

        ---
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        주소 데이터 변경

        `http://13.209.33.72/users/{user_pk}/address/{id}` patch
        -----

        해당 요청은 주문서 - 배송지 입력 및, 마이컬리 - 배송지 변경에서 사용을 할 수 있습니다.

        받는 분 이름, 받는 분 휴대폰은 모델링에서 고려를 하지 못했습니다.

        아래 시리얼라이저를 참고하여 수정을 원하는 데이터를 넘겨주시면 됩니다.

        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        주소 삭제

        ----
        토큰이 필요하지 않습니다.
        """
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def order(self, request, *args, **kwargs):
        """
        User Order Address API 주문서 작성 시, 새로운 주소를 생성할 경우에 사용하는 api

        ---
        배송지 생성 api endpoint

        `13.209.33.72/api/users/<user PK>/address/order`

        `Authorizations : token 88f0566e6db5ebaa0e46eae16f5a092610f46345`
        """
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)


class UserSearchViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = UserSearch.objects.all()
    serializer_class = UserSearchSerializer
    swagger_schema = MyAutoSchema

    def get_queryset(self):
        try:
            if self.kwargs['user_pk']:
                return self.queryset.filter(user_id=self.kwargs['user_pk']).order_by('-keyword__updated_at')
        except KeyError:
            return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['list']:
            return UserSearchListSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        유저 최근 검색어 api

        ----
        """
        return super().list(request, *args, **kwargs)

    @action(detail=False, )
    def popular_word(self, request, *args, **kwargs):
        """
        검색 - 인기검색어 API

        ---

        모든 검색어 중 가장 많이 검색된 검색어 순으로 상위 다섯 개 까지만 나열합니다.
        """
        orderby_word = KeyWord.objects.all().order_by('-count')[:5]
        serializer = PopularSerializer(orderby_word, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
