from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.db.models import CASCADE, F
from goods.models import Goods

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    quantity_of_goods = models.IntegerField('총 상품 수량', default=0)

    @property
    def total_pay(self):
        payment = 0
        for ins in self.items.all():
            payment += ins.sub_total
        return payment

    @property
    def discount_total_pay(self):
        payment = 0
        for ins in self.items.all():
            if ins.discount_payment is not None:
                payment += ins.discount_payment
            else:
                payment += ins.sub_total
        return payment


class CartItem(models.Model):
    class Order_Status(models.TextChoices):
        DEPARTURE = 'w', ('대기')
        COMPLETE = 'c', ('완료')
        REVIEW = 'r', ('후기작성완료')

    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    cart = models.ForeignKey(Cart, on_delete=CASCADE, related_name='items', null=True, blank=True)
    goods = models.ForeignKey(Goods, on_delete=CASCADE, related_name='items', )
    order = models.ForeignKey('order.Order', on_delete=models.SET_NULL, null=True, related_name='items', )
    status = models.CharField('배송 상태', max_length=1, default=Order_Status.DEPARTURE, choices=Order_Status.choices)

    @property
    def sub_total(self):
        return int(self.goods.price * self.quantity)

    @property
    def discount_payment(self):
        try:
            if type(self.goods.sales.discount_rate) is int:
                each = (100 - self.goods.sales.discount_rate) * 0.01 * self.goods.price
                quantity = int(each * self.quantity)
                return quantity
            return self.sub_total
        except AttributeError:
            return self.sub_total

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.id is None:
            self.cart.quantity_of_goods = F('quantity_of_goods') + 1
            self.cart.save()
        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, using=None, keep_parents=False):
        super().delete()
        self.cart.quantity_of_goods = F('quantity_of_goods') - 1
        self.cart.save()
