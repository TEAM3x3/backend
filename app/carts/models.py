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
    cart = models.ForeignKey(Cart, on_delete=CASCADE, related_name='item', null=True)
    goods = models.ForeignKey(Goods, on_delete=CASCADE)
    quantity = models.IntegerField(default=1,
                                   validators=[MinValueValidator(1), MaxValueValidator(50)])

    class Meta:
        db_table = 'CartItem'

    # 장바구니 합계
    def sub_total(self):
        return self.goods.price * self.quantity
