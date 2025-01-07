from django.contrib import admin
from django.conf import settings

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'fio', 
        'phone_number', 
        'telegram_id',
        'username', 
    )
    list_editable = (
        'phone_number',
    )
    
    readonly_fields = (
        'telegram_id',
        'username', 
        'bot_start_link',
    )    
 