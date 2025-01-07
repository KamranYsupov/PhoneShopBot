from asgiref.sync import sync_to_async
from django.db import transaction
 
from models import (
    TelegramUser, 
    CartItem,
    Device,
    Order,
    OrderItem
)
from orm.cart import clear_cart


@sync_to_async
def create_order(
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

    with transaction.atomic():
        order_data = {'buyer_id': telegram_user.id}
        if comment:
            order_data['comment'] = comment
            
        order = Order.objects.create(**order_data)

        for cart_item in telegram_user.cart.all():
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

        if updated_devices:
            Device.objects.bulk_update(updated_devices, ['quantity'])
        if order_items:
            OrderItem.objects.bulk_create(order_items)
        CartItem.objects.filter(
            telegram_user_id=telegram_user.id
        ).delete()

        return order