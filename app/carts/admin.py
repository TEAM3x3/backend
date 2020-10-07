from django.contrib import admin
from carts.models import CartItem, Cart


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'goods', 'quantity', 'order', 'status']


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
