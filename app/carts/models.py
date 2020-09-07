from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE
from goods.models import Goods

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    @property
    def total_pay(self):
        payment = 0
        for ins in self.item.all():
            payment += ins.sub_total()
        return payment


class CartItem(models.Model):
    quantity = models.IntegerField(default=1,
                                   validators=[MinValueValidator(1), MaxValueValidator(50)])
    cart = models.ForeignKey(Cart, on_delete=CASCADE, related_name='item', null=True)
    goods = models.ForeignKey(Goods, on_delete=CASCADE)
    order = models.ForeignKey('order.Order',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='item',
                              )

    def sub_total(self):
        return self.goods.price * self.quantity
