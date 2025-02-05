from django.contrib import admin
from django.utils.html import format_html

from .models import Order, OrderItem
from bot.utils.message import get_item_info_message


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = (
        'device_supplier',
        'device',
        'price_for_one', 
        'x_string',
        'quantity',
        'equal_string',
        'general_price', 
    )
    readonly_fields = (
        'device_supplier', 
        'device',
        'x_string',
        'equal_string',
        'general_price',
    )
    extra = 1
    
    def has_add_permission(self, request, obj=None):
        return False
    
    @admin.display(description='',)
    def x_string(self, obj):
        return format_html('<b>×</b>')
    
    @admin.display(description='',)
    def equal_string(self, obj):
        return format_html('<b>=</b>')
    
    @admin.display(description='Общая стоимось',)
    def general_price(self, obj):
        return format_html(f'<b>{obj.general_price} $</b>')
    
    @admin.display(description='Поставщик',)
    def device_supplier(self, obj):
        return obj.device.supplier.name
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'number', 
        'status', 
        'total_price',
        'buyer',
    )
    list_editable = ('status', )
    
    search_fields = [
        'number__iregex'
    ]
    fields = (
        'short_info',
        'status',
        'number',
        'total_price',
        'buyer', 
        'comment',
        'created_at',
    )
    readonly_fields = (
        'short_info',
        'number',
        'total_price',
        'buyer', 
        'comment',
        'created_at',
    )
    
    inlines = (OrderItemInline, )
    
    def has_add_permission(self, request):
        return False 
    
    @admin.display(description='Итого',)
    def total_price(self, obj):
        total_price = sum([
            item.general_price 
            for item in obj.items.all()
        ])
        
        return str(total_price)
    
    @admin.display(description='Краткая информация',)
    def short_info(self, obj):
        short_info = ''
        for item in obj.items.select_related('device'):
            short_info += (
                f'{item.device.name} '
                f'{item.price_for_one}×{item.quantity}<br>'
            )
            
        short_info += '<br>'
        if obj.buyer.username:
            short_info += (
                f'<a href="https://t.me/{obj.buyer.username}">'
                f'@{obj.buyer.username}</a>'
            )
        else:
            short_info += f'{obj.buyer}</b>'
        
        return format_html(short_info)