from django.contrib import admin

# Register your models here.
from goods.models import Goods, GoodsDetail, Type, Category, GoodsType, GoodsExplain


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


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


admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsDetail, GoodsDetailAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(GoodsExplain, GoodsExplainAdmin)