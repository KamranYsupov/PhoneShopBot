from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('device_supplier', 'device', 'price_string', 'quantity', )
    readonly_fields = ('device_supplier', 'device', 'price_string')
    extra = 1
    
    def has_add_permission(self, request, obj=None):
        return False
    
    @admin.display(description='Цена',)
    def price_string(self, obj):
        return f'{obj.quantity} шт × {obj.price_for_one} = {obj.general_price} $'
    
    @admin.display(description='Поставщик',)
    def device_supplier(self, obj):
        return obj.device.supplier.name
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'status', 'total_price', 'buyer')
    list_editable = ('status', )
    
    search_fields = [
        'number__iregex'
    ]
    readonly_fields = (
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