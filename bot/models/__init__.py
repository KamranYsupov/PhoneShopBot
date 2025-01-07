__all__ = (
    'TelegramUser',
    'Order',
    'OrderItem',
    'DeviceCompany',
    'DeviceModel',
    'DeviceSeries', 
    'Device',
)


from web.apps.telegram_users.models import TelegramUser
from web.apps.orders.models import Order, OrderItem
from web.apps.devices.models import (
    DeviceCompany,
    DeviceModel,
    DeviceSeries, 
    Device
)
