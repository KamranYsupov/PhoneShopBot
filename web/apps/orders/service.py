from datetime import date

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone

from web.apps.devices.models import Device
from web.apps.telegram_users.models import TelegramUser, CartItem
from .models import Order, OrderItem
from ...services.telegram_service import telegram_service
from ...utils.requests import verify_status_code


def create_order_from_cart(
    telegram_id: TelegramUser.telegram_id,
    comment: str | None = None,
) -> Order | list[CartItem] | None:
    try:
        telegram_user = (
            TelegramUser.objects
            .prefetch_related('cart__device')
            .get(telegram_id=telegram_id)
        )
    except ObjectDoesNotExist:
        return  

    invalid_cart_items = []
    order_items = []
    updated_devices = []
    cart_items = telegram_user.cart.all()
    
    if not cart_items:
        return 
    
    with transaction.atomic():
        order_data = {'buyer_id': telegram_user.id}
        if comment:
            order_data['comment'] = comment
            
        order = Order.objects.create(**order_data)

        for cart_item in cart_items:
            device = cart_item.device
            if device.quantity < cart_item.quantity:
                invalid_cart_items.append(cart_item)
                continue

            order_items.append(OrderItem(
                order_id=order.id,
                device_id=cart_item.device_id,
                quantity=cart_item.quantity
            ))

            device.quantity -= cart_item.quantity
            updated_devices.append(device)

        if invalid_cart_items:
            order.delete()
            return invalid_cart_items
            
        if not order_items:
            order.delete()
            return
        
        for item in order_items:
            item.price_for_one = item.get_price_for_one() # Вручную вычисляем price_for_one для каждого обьекта
        
        Device.objects.bulk_update(updated_devices, ['quantity'])
        OrderItem.objects.bulk_create(order_items)
        CartItem.objects.filter(
            telegram_user_id=telegram_user.id
        ).delete()

        return order


def send_orders_info(
    telegram_id: int = settings.ANALYTIC_RECEIVER_TELEGRAM_ID,
    day: date | None = None
):
    """Функция для отправки информации о заказах за день"""
    if day is not None:
        day =  timezone.now().date()

    orders = (
        Order.objects
            .prefetch_related('items')
            .filter(
                status__in=(Order.Status.BOUGHT, Order.Status.CHANGED),
                created_at=day,
            )
    )
    order_items = []
    for order in orders:
        order_items.extend(list(order.items.all()))

    total_price = sum([item.general_price for item in order_items])

    sold_devices_count = 0
    for item in order_items:
        sold_devices_count += item.quantity

    formated_date = day.strftime('%d.%m.%Y')
    message_text = (
        f'<b><em>Аналитика на {day.strftime(formated_date)}</em></b>:\n\n'
        f'<em>Общее количество проданных устройств</em>: <b>{sold_devices_count}</b>\n'
        f'<em>Выручка</em>: <b>{total_price} $</b>'
    )
    response = telegram_service.send_message(
        chat_id=telegram_id,
        text=message_text,
    )

    return verify_status_code(response)