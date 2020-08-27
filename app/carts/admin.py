from django.contrib import admin
from carts.models import CartItem


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'quantity', ]


admin.site.register(CartItem, CartItemAdmin)
