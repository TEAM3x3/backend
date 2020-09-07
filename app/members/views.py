import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from members.serializers import UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
