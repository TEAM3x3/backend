from django.utils import timezone

from carts.models import CartItem
from datetime import datetime, timedelta


def cron_job():
    """
    22시에 크론탭 코드를 실행할 때 전날 22시부터 오늘 14시까지 상품을 변경
    """
    qs = CartItem.objects.filter(
        status='w',
        order__orderdetail__created_at__gt=datetime.now(tz=timezone.utc) - timedelta(hours=16),
        order__orderdetail__created_at__lt=datetime.now(tz=timezone.utc) - timedelta(hours=8)
    )
    for ins in qs:
        ins.status = 'c'
        ins.save()
