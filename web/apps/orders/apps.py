from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web.apps.orders'
    verbose_name = 'Управление заказами'
    
    def ready(self):
        import web.apps.orders.signals
