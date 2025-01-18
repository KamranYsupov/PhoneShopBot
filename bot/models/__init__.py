__all__ = (
    'TelegramUser',
    'CartItem',
    'Order',
    'OrderItem',
    'DeviceCompany',
    'DeviceModel',
    'DeviceSeries', 
    'Device',
)


from web.apps.telegram_users.models import (
    TelegramUser,
    CartItem,
)
from web.apps.orders.models import Order, OrderItem
from web.apps.devices.models import (
    DeviceCompany,
    DeviceModel,
    DeviceSeries, 
    Device
)
