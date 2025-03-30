from django.contrib import admin

from .models import Notification, NotificationTemplate


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    search_fields = (
        'name__iregex', 
        'text__iregex',
    )
    readonly_fields = ('created_at', )
    
    filter_horizontal = ('receivers', )    
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    search_fields = (
        'name__iregex',
        'text__iregex',
    )
    readonly_fields = ('created_at',)

    