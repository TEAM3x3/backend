from django.contrib import admin
from carts.models import CartItem


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'goods', 'quantity', ]


admin.site.register(CartItem, CartItemAdmin)
