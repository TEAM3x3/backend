from django.contrib import admin
from carts.models import Cart, CartItem


class CartsAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'created_at',]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'quantity',]

admin.site.register(Cart, CartsAdmin)
admin.site.register(CartItem, CartItemAdmin)