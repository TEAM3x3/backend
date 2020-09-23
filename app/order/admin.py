from django.contrib import admin

# Register your models here.
from order.models import Order, OrderReview, OrderDetail


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', ]


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', ]


@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'goods']
