from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE
from goods.models import Goods

User = get_user_model()

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['created_at']


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    goods = models.ForeignKey(Goods, on_delete=CASCADE)
    quantity = models.IntegerField(default=1,
                                   validators=[MinValueValidator(1), MaxValueValidator(50)])

    class Meta:
        db_table = 'CartItem'

    # 장바구니 합계
    def sub_total(self):
        return self.goods.price * self.quantity