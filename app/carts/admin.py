from django.contrib import admin
from carts.models import CartItem, Cart


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'goods', 'quantity', ]


class CartAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', ]


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
