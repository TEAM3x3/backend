from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from goods.models import Goods

# https://dev-mht.tistory.com/147
User = get_user_model()


class Cart(models.Model):
    cart_id = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True, default=1,
                                           validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '장바구니'
        verbose_name_plural = f'{verbose_name}목록'
        ordering = ['-pk']

    # 장바구니에 담긴 각 상품의 합계
    def sub_total(self):
        return self.goods.price * self.quantity

    def __str__(self):
        return self.goods.title
