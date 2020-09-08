from django.contrib import admin
from django.contrib.auth import get_user_model
from members.models import UserAddress

User = get_user_model()


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'nickname', 'address',]


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'detail_address', 'require_message', 'status',
                  'recieving_place', 'entrance_password', 'free_pass', 'etc', 'message']


admin.site.register(User, UserAdmin)
admin.site.register(UserAddress, UserAddressAdmin)


