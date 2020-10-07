from django.contrib.auth import get_user_model
from django.db import models, transaction

from goods.models import Goods

User = get_user_model()


def review_img(instance, filename):
    import datetime
    data = datetime.datetime.now().strftime('/%y/%m/%d') + filename
    return data


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

    class Payment_Type(models.TextChoices):
        KAKAO = '카카오페이', ('카카오페이')

    """
    1. 결제 정보 - 상품 금액(total_payment), 배송비, 상품 할인 금액(discount_price), 쿠폰 할인, 결제 금액(discount_payment), 적립 금액(point)
    2. 주문 정보 - 주문 번호( order.id), 주문자 명 (request.user), 보내는 분 (request.user), 결제 일시 (order.created_at)
    3. 배송지 정보 -
    """
    title = models.CharField(max_length=50, null=True, blank=True)
    delivery_cost = models.PositiveIntegerField(default=0, null=True, help_text='배송비')
    point = models.PositiveIntegerField(default=0, help_text='적립 금액')
    created_at = models.DateTimeField(auto_now_add=True, help_text='결제 일시')
    status = models.CharField(max_length=4, choices=Order_Status.choices, default=Order_Status.PAYMENT_WAIT,
                              help_text='주문 상태')
    # 2. 주문 정보
    consumer = models.CharField(max_length=10, help_text='주문자 명', null=True)

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
    etc = models.CharField(max_length=200, help_text='공동현관 기타', null=True, )

    # 경비실, 택배함, 기타장소 특이사항
    extra_message = models.TextField(help_text='특이사항, 택배함 정보', null=True)

    # 배송 완료 메세지 전송

    message = models.BooleanField(help_text='배송 완료 메세지 전송 True면 직후, False면 오전 7시')

    # 결제 정보
    payment_type = models.CharField(choices=Payment_Type.choices, help_text='결제 정보', null=True, max_length=10,
                                    default=Payment_Type.KAKAO)

    """
    # 질문 , 강사님이 perform create 의 경우 값을 넣으라고 하셨던 말씀이 기억나서 해 보았는데, {{local}}/api/users/1/orders 의 경우 
    view에서 nested의 값을 받고, 
        def perform_create(self, serializer):
            order_instance = Order.objects.get(pk=self.kwargs['order_pk'])
            serializer.save(order=order_instance)
    로 하고 serializers fields 에서는 order 에 대한 필드를 넣지 않고 생성하여 구현하였습니다. 말씀하신게 맞나요???
    """
    order = models.OneToOneField(
        'order.Order',
        on_delete=models.CASCADE,
    )


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
    img = models.ImageField(upload_to=review_img, null=True, help_text='이미지 필드')
    # 회원 탈퇴한 유저라면 null 허용 , default로 해서 탈퇴한 유저 전용 instance 를 만드는게 나은지
    user = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews'
    )
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    cartItem = models.ForeignKey(
        'carts.CartItem',
        on_delete=models.CASCADE,
        # 리뷰 더미값들을 위해서
        null=True,
        related_name='reviews'
    )

    @staticmethod
    def created_mocking():
        user_lst = []
        for index in range(5):
            user = User.objects.create_user(username=f'user{index}', password='1111', nickname=f'nickname{index}',
                                            email=f'mail{index}@mail.com',
                                            phone='111-2222-3333',
                                            )
            user_lst.append(user)
        Goods_lst = Goods.objects.all()[:5]
        title_lst = [
            '잘 먹었습니다. ',
            '너무 맛있었어요',
            '다음에 또 시키도록 하겠습니다.',
            '맛있어서 리뷰 달았어요',
            '추천합니다!!!!!!!'
        ]
        content_lst = [
            '잘 먹었습니다. 에 대한 내용입니다.',
            '너무 맛있었어요 에 대한 내용입니다.',
            '다음에 또 시키도록 하겠습니다. 에 대한 내용입니다.',
            '맛있어서 리뷰 달았어요 에 대한 내용입니다.',
            '추천합니다!!!!!!! 에 대한 내용입니다.'
        ]
        for goods in Goods_lst:
            for index in range(5):
                OrderReview.objects.create(
                    title=title_lst[index],
                    content=content_lst[index],
                    user=user_lst[index],
                    goods=goods
                )
