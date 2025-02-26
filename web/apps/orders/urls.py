from django.urls import path
from web.apps.orders.views import send_orders_info_view

urlpatterns = [
    path('send-orders-info/', send_orders_info_view, name='send_orders_info'),
]