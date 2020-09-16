from django.contrib import admin

# Register your models here.
from order.models import Order, OrderReview


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'address']


@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'goods']
