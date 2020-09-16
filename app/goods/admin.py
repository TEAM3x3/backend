from django.contrib import admin
from goods.models import Goods, GoodsDetail, Type, Category, GoodsType, GoodsExplain, DeliveryInfoImageFile, \
    DeliveryInfoImageImageFile, SaleInfo


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'packing_status', 'sales']


class GoodsDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods']


class GoodsExplainAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_title', 'goods']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'goods', ]


class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'address_img']


class DeliveryInfoImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'info']


class SaleInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'discount_rate', 'contents']


admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsDetail, GoodsDetailAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(GoodsExplain, GoodsExplainAdmin)
admin.site.register(DeliveryInfoImageFile, DeliveryInfoAdmin)
admin.site.register(DeliveryInfoImageImageFile, DeliveryInfoImageAdmin)
admin.site.register(SaleInfo, SaleInfoAdmin)
