from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from members.models import UserAddress
from members.permissions import UserInfoOwnerOrReadOnly
from members.serializers import UserSerializer, UserAddressSerializers

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserInfoOwnerOrReadOnly,)

    def get_permissions(self):
        if self.action in ['user_info', ]:
            return [UserInfoOwnerOrReadOnly()]
        return super().get_permissions()

    @action(detail=False)
    def check_username(self, request):
        username = request.query_params.get('username')
        user = User.objects.filter(username=username)
        if user:
            return Response({"message": "이미 사용중인 ID입니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "사용가능한 ID입니다."}, status=status.HTTP_200_OK)

    @action(detail=False)
    def check_email(self, request):
        email = request.query_params.get('email')
        user = User.objects.filter(email=email)
        if user:
            return Response({"message": "이미 사용중인 email입니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "사용가능한 email입니다."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = User.objects.get(username=request.data.get('username'))
        if user.check_password(request.data.get('password')):
            token, __ = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        user = request.user
        user.auth_token.delete()
        return Response({"clear"}, status=status.HTTP_200_OK)

    @action(detail=False)
    def user_info(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        if user.check_password(request.data.get('password')):
            profile = User.objects.filter(username=user.username)
            serializer = UserSerializer(profile, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'])
    def password_change(self, request):
        user = User.objects.get(username=request.user.username)
        user.set_password(request.data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserAddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializers

    def get_queryset(self):
        try:
            if self.kwargs['user_pk']:
                return self.queryset.filter(user_id=self.kwargs['user_pk'])
        except KeyError:
            return super().get_queryset()
