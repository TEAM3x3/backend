from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'None'),
    )
    nickname = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField('핸드폰 번호', max_length=15)
    gender = models.CharField('성별', max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField(max_length=11, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')

    def save(self, *args, **kwargs):
        from carts.models import Cart
        if self.pk is None:
            super().save(*args, **kwargs)
            Cart.objects.create(user=self)
        else:
            super().save(*args, **kwargs)
    # REQUIRED_FIELDS = ['email']


class UserAddress(models.Model):
    LOCATION_CHOICE = (
        ('FD', 'Front Door'),
        ('SO', 'Security Office'),
        ('DB', 'Delivery Box'),
        ('etc', 'etc'),
    )
    address = models.CharField(max_length=200)
    detail_address = models.CharField(max_length=200)
    require_message = models.CharField('요청 사항', max_length=100)
    status = models.CharField('기본 배송지', max_length=1, default=False)
    recieving_place = models.CharField('받으실 장소', max_length=3, choices=LOCATION_CHOICE, null=True)
    entrance_password = models.CharField('공동현관 비밀번호', max_length=10, null=True)
    free_pass = models.BooleanField('공동현관 자유출입 가능 여부', default=False)
    etc = models.CharField('기타', max_length=100, null=True)
    message = models.BooleanField('배송완료 메시지 전송 여부', default=False, null=True)

    user = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
        related_name='address',
    )

    def save(self, *args, **kwargs):
        if self.status == 'T':
            address_data = UserAddress.objects.filter(user=self.user).exclude('F')
            print(address_data)
        # else:
        #     super().save(*args, **kwargs)




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
