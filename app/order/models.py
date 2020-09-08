from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    address = models.ForeignKey(
        'members.UserAddress',
        on_delete=models.CASCADE,
    )
    status = models.CharField('배송 상태', max_length=1)

    def total_payment(self):
        payment = 0
        for ins in self.item.all():
            payment += ins.sub_total()
        return payment


class OrderReview(models.Model):
    """
    1. 주문이 완료된 상품은 리뷰를 달 수 있다.
    2. order의 status가 "D" - Departure // "P" - Progress // "C" - Complete
    3. order의 status가 C라면 리뷰 생성 가능.
    4. Review 작성 완료 후에는 "R"
    5 . cartitem과 review는 unique together?
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    title = models.CharField(max_length=128)
    content = models.TextField()
    cartitem = models.ForeignKey(
        'carts.CartItem',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'members.User',
        on_delete=models.SET_NULL,
        null=True,
    )
