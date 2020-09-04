from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class OrderItem(models.Model):
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.CASCADE,
        related_name='item',
    )
    goods = models.ForeignKey(
        'goods.Goods',
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()

    def sub_total(self):
        return self.goods.price * self.quantity


class Order(models.Model):
    order_date = models.DateTimeField(
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

    def total_payment(self):
        payment = 0
        for ins in self.item.all():
            payment += ins.sub_total()
        return payment
