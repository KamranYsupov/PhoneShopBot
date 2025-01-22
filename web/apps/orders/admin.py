from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('device', 'quantity')
    readonly_fields = ('device', 'quantity')
    extra = 1
    
    def has_add_permission(self, request, obj=None):
        return False
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'status', 'buyer')
    list_editable = ('status', )
    
    search_fields = [
        'number__iregex'
    ]
    readonly_fields = (
        'number',
        'buyer', 
        'comment',
        'created_at',
    )
    
    inlines = (OrderItemInline, )
    
    def has_add_permission(self, request):
        return False 