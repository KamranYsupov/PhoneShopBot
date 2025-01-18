from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('device', 'quantity')
    extra = 1
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('number', 'created_at',)
    
    inlines = (OrderItemInline, )