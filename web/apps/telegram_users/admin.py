from django.contrib import admin
from django.conf import settings

from .models import TelegramUser, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ('device', 'quantity')
    extra = 0


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'fio', 
        'telegram_id',
        'username', 
        'bot_start_link', 
        'phone_number',
    )
    list_editable = (
        'phone_number',
    )
    
    readonly_fields = (
        'telegram_id',
        'username', 
        'bot_start_link',
    )
    
    def change_list_view(self, request, extra_context=None):
        print('change_list_view')
        my_custom_data = "Это мои данные"

        extra_context = extra_context or {}
        extra_context['my_custom_data'] = my_custom_data

        return super().change_list_view(request, extra_context=extra_context)
    
    inlines = (CartItemInline, )    
 