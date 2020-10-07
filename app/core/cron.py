from django.utils import timezone

from carts.models import CartItem
from datetime import datetime, timedelta


def cron_job():
    qs = CartItem.objects.filter(status='w',
                                 order__orderdetail__created_at__gt=datetime.now(tz=timezone.utc)
                                                                    - timedelta(hours=16))
    for ins in qs:
        ins.status = 'w'
        ins.save()
