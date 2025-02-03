from django.contrib import admin
from django.conf import settings
from django.db.utils import OperationalError

from web.apps.bot_settings.models import BotSettings    
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
    
    def changelist_view(self, request, extra_context=None):
        bot_is_active = BotSettings.get_instance().is_active

        extra_context = extra_context or {}
        extra_context['bot_is_active'] = bot_is_active

        return super().changelist_view(request, extra_context=extra_context)
    
    inlines = (CartItemInline, )    
 