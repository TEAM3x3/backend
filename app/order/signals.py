from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from order.models import Order


@transaction.atomic
@receiver(post_save, sender=Order)
def order_post_save(sender, **kwargs):
    """
    결제가 붙게 된다면 결제 코드를 넣는다.
    결제가 완료 된 후에 order의 status 변수 값을 변경 후
    cart_item.cart = None으로 변경.
    * 결제 중 에러가 난다면 order create 자체가 취소? -> 주문서 생성과 결제 API endpoint를 구분
   """
    pass
