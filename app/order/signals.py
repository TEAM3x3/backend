from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from order.models import OrderReview


@transaction.atomic
@receiver(post_save, sender=OrderReview)
def orderReview_post_save(sender, **kwargs):
    """
    댓글을 작성 한 후 해당 리뷰와 relation을 가진 cartitem의 status 변경
    시그널 출처 : https://dgkim5360.tistory.com/entry/django-signal-example
   """
    try:
        cartItem_instance = kwargs['instance'].cartItem
        cartItem_instance.status = 'r'
        cartItem_instance.save()
    except AttributeError:
        pass
