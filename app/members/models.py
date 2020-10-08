import base64
import datetime
import hashlib
import hmac
import json
import secrets
import time

import requests
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Gender_Choice(models.TextChoices):
        MALE = 'M', ('Male')
        FEMALE = 'F', ('Female')
        NONETYPE = 'N', ('None')

    nickname = models.CharField(max_length=20, help_text='본명')
    email = models.EmailField(unique=True)
    phone = models.CharField('핸드폰 번호', max_length=15)
    gender = models.CharField('성별', max_length=1, choices=Gender_Choice.choices, default=Gender_Choice.NONETYPE)
    birthday = models.DateField(max_length=11, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')

    def save(self, *args, **kwargs):
        from carts.models import Cart
        if self.id is None:
            super().save(*args, **kwargs)
            Cart.objects.create(user=self)
        else:
            super().save(*args, **kwargs)
    # REQUIRED_FIELDS = ['email']


class UserAddress(models.Model):
    class Receiving_Choice(models.TextChoices):
        FRONT_DOOR = '문 앞', ('문 앞')
        SEQURITY_OFFICE = '경비실', ('경비실')
        DELIVERY_BOX = '택배함', ('택배함')
        ETC = '기타 장소', ('기타')

    class AddressStatus(models.TextChoices):
        NORMAL = 'T', ('기본 배송지')
        INSTANT = 'F', ('일회성 배송지')

    address = models.CharField(max_length=200, help_text='주소')
    detail_address = models.CharField(max_length=200, help_text='상세주소')
    status = models.CharField(choices=AddressStatus.choices, max_length=1, help_text='기본 배송지 상태')
    receiving_place = models.CharField(max_length=5,
                                       choices=Receiving_Choice.choices,
                                       default=Receiving_Choice.ETC,
                                       null=True,
                                       help_text='받으실 장소',
                                       )
    entrance_password = models.CharField(max_length=10, null=True, help_text='공동현관 비밀번호', )
    free_pass = models.BooleanField(default=False, help_text='공동현관 자유출입 가능 여부 값을 넣지 않으면 default 값은 False입니다.', )
    etc = models.CharField(max_length=100, null=True, help_text='기타', )
    message = models.BooleanField(default=False, null=True, help_text='배송완료 메시지 전송 여부', )
    extra_message = models.CharField(max_length=200, null=True,
                                     help_text='경비실, 택배함, 기타장소 텍스트 정보 receiving_place의 값에 영향을 받음')

    user = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
        related_name='address',
    )


class UserSearch(models.Model):
    user = models.ForeignKey('members.User', on_delete=models.CASCADE, related_name='search')
    keyword = models.ForeignKey('members.Keyword', on_delete=models.CASCADE, related_name='search')
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        count_word = self.keyword
        if count_word:
            self.keyword.count += 1
            self.keyword.save()
            super().save(*args, **kwargs)


class KeyWord(models.Model):
    name = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0, db_index=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

# class AuthPhoneNum(models.Model):
#     phone_number = models.CharField(max_length=11)
#     registration_id = models.CharField(
#         verbose_name='주민등록번호',
#         max_length=7,
#     )
#     auth_number = models.IntegerField()
#     ttl = models.DateTimeField()
#
#     def save(self, *args, **kwargs):
#         self.auth_number = secrets.choice(range(100000, 999999))
#         self.ttl = timezone.now() + datetime.timedelta(minutes=5)
#         super().save(*args, **kwargs)
#
#         self.send_sms()
#
#     def send_sms(self):
#         timestamp = int(time.time() * 1000)
#         timestamp = str(timestamp)
#
#         url = "https://sens.apigw.ntruss.com"
#         requestUrl1 = "/sms/v2/services/"
#         requestUrl2 = "/messages"
#         serviceId = "ncp:sms:kr:260483911484:sofastcar_sms"
#         access_key = "RcSVHr6YgMHKg38rmR4X"
#
#         uri = requestUrl1 + serviceId + requestUrl2
#         apiUrl = url + uri
#
#         secret_key = "7PWFNRn7Md46Dgegpf8MAncOaSPH4ReDICyJf4xZ"
#         secret_key = bytes(secret_key, 'UTF-8')
#         method = "POST"
#         message = method + " " + uri + "\n" + timestamp + "\n" + access_key
#         message = bytes(message, 'UTF-8')
#
#         signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
#
#         messages = {"to": f"{self.phone_number}"}
#         body = {
#             "type": "SMS",
#             "contentType": "COMM",
#             "from": "01063855074",
#             "subject": "subject",
#             "content": f"[인증번호]: {self.auth_number}",
#             "messages": [messages]
#         }
#         body2 = json.dumps(body)
#
#         headers = {
#             'Content-Type': 'application/json; charset=utf-8',
#             'x-ncp-apigw-timestamp': timestamp,
#             'x-ncp-iam-access-key': access_key,
#             'x-ncp-apigw-signature-v2': signingKey
#         }
#
#         requests.post(apiUrl, headers=headers, data=body2)

# class Profile(models.Model):

#     COUPON_CHOICES = (
#         ('A', '[신규가입쿠폰] 10% 할인'),
#         ('B', '[농할갑시다] 햇농산물 20%'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     grade = models.OneToOneField(User, on_delete=models.CASCADE)
#     coupon = models.CharField('쿠폰', max_length=1, choices=COUPON_CHOICES)
#     accumulated_money = models.IntegerField('적립금', default=0)
#     point = models.IntegerField('포인트', default=0)
