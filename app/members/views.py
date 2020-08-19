from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from members.serializers import UserSerializers

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #
    #     data = request.data
    #
    #     if data['password'] != data['password_check']:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        return Response({"detail": "logged out."}, status=status.HTTP_200_OK)
