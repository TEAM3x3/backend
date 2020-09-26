from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    @property
    def total_payment(self):
        payment = 0
        for ins in self.items.all():
            payment += ins.sub_total
        return payment

    @property
    def discount_payment(self):
        payment = 0
        for ins in self.items.all():
            payment += ins.discount_payment
        return payment


class OrderDetail(models.Model):
    class Order_Status(models.TextChoices):
        PAYMENT_WAIT = '결제대기', ('결제 대기')
        PAYMENT_COMPLETE = '결제완료', ('결제 완료')
        DELIVERY_READY = '배송준비', ('배송 준비')
        DELIVERY_COMPLETE = '배송완료', ('배송 완료')

    class Delivery_Type(models.TextChoices):
        COMMON_POST = '샛별배송', ('샛별배송')
        POST = '택배배송', ('택배배송')

    class Location_Choice(models.TextChoices):
        FRONT_DOOR = '문 앞', ('문 앞')
        SEQURITY_OFFICE = '경비실', ('경비실')
        DELIVERY_BOX = '우편함', ('우편함')
        ETC = '기타', ('기타')

    class Message_Choice(models.TextChoices):
        RIGHT_AFTER = '직후', ('직후')
        AM_7 = '오전7시', ('오전 7시')

    class Payment_Type(models.TextChoices):
        KAKAO = '카카오페이', ('카카오페이')

    """
    1. 결제 정보 - 상품 금액(total_payment), 배송비, 상품 할인 금액(discount_price), 쿠폰 할인, 결제 금액(discount_payment), 적립 금액(point)
    2. 주문 정보 - 주문 번호( order.id), 주문자 명 (request.user), 보내는 분 (request.user), 결제 일시 (order.created_at)
    3. 배송지 정보 -
    """
    delivery_cost = models.PositiveIntegerField(default=0, null=True, help_text='배송비')
    point = models.PositiveIntegerField(default=0, help_text='적립 금액')
    created_at = models.DateTimeField(auto_now_add=True, help_text='결제 일시')
    status = models.CharField(max_length=4, choices=Order_Status.choices, default=Order_Status.PAYMENT_WAIT,
                              help_text='주문 상태')
    # 2. 주문 정보
    consumer = models.CharField(max_length=10, help_text='주문자 명')

    # 3. 배송지 정보 문자열로 저장
    receiver = models.CharField(max_length=30, help_text='받는 분')
    receiver_phone = models.CharField(max_length=20, help_text='받는 분 번호')
    delivery_type = models.CharField(choices=Delivery_Type.choices, max_length=4)
    zip_code = models.CharField(max_length=10, help_text='우편 번호')
    address = models.CharField(max_length=200, help_text='주소')

    # 4. 받으실 장소
    receiving_place = models.CharField(max_length=3, choices=Location_Choice.choices, help_text='받으실 장소')
    entrance_password = models.CharField(max_length=10, help_text='공동현관 비밀번호', null=True, )
    free_pass = models.BooleanField(default=False, help_text='공동 현관 자유 출입 가능')
    etc = models.CharField(max_length=200, help_text='공동현관 기타', null=True)

    # 경비실, 택배함, 기타장소 특이사항
    extra_message = models.TextField(help_text='특이사항, 택배함 정보', null=True)

    # 배송 완료 메세지 전송

    message = models.CharField(choices=Message_Choice.choices, max_length=5, help_text='배송 완료 메세지 전송')

    # 결제 정보
    payment_type = models.CharField(choices=Payment_Type.choices, help_text='결제 정보', null=True, max_length=10)
    order = models.OneToOneField(
        'order.Order',
        on_delete=models.CASCADE,
    )


#
# class Payment(models.Model):
#     """
#     결제에 대한 데이터 생성 후,  order OTO 로 참조.
#     """
#     order = models.OneToOneField('order.Order')


class OrderReview(models.Model):
    """
    1. 주문이 완료된 상품은 리뷰를 달 수 있다.
    2. order의 status가 "D" - Departure // "P" - Progress // "C" - Complete
    3. order의 status가 C라면 리뷰 생성 가능.
    4. Review 작성 완료 후에는 "R"
    5 . cartitem과 review는 unique together?
    """
    created_at = models.DateTimeField(auto_now_add=True, )
    title = models.CharField(max_length=128)
    content = models.TextField()
    # 회원 탈퇴한 유저라면 null 허용 , default로 해서 탈퇴한 유저 전용 instance 를 만드는게 나은지
    user = models.ForeignKey(
        'members.User',
        on_delete=models.SET_NULL,
        null=True
    )
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
    )
    cartItem = models.ForeignKey(
        'carts.CartItem',
        on_delete=models.CASCADE,
    )
