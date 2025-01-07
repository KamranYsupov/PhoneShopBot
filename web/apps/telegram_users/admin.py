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
    
    inlines = (CartItemInline, )    
 