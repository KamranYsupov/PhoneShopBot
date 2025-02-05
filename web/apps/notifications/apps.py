from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web.apps.notifications'
    verbose_name = 'Рассылки'
    
    def ready(self):
        import web.apps.notifications.signals
