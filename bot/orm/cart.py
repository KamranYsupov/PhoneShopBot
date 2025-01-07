from asgiref.sync import sync_to_async

from models import (
    TelegramUser, 
    CartItem,
    Device
)
from utils.validators import validate_quantity

from typing import Any

@sync_to_async
def add_to_cart(
    device_id: Device.id,
    telegram_user_id: TelegramUser.id, 
    quantity: int,
) -> CartItem | None:
    cart_item, created = CartItem.objects.get_or_create(
        device_id=device_id,
        telegram_user_id=telegram_user_id,
        defaults={'quantity': quantity}  
    )

    if not created:
        cart_item.quantity = quantity
        cart_item.save()  

    return cart_item


@sync_to_async
def get_cart_quantity(
    device_id: Device.id,
    telegram_user_id: TelegramUser.id, 
) -> int:
    cart_quantity = sum(
        CartItem.objects.filter(
            device_id=device_id,
            telegram_user_id=telegram_user_id
        ).values_list('quantity', flat=True)
    )
    
    return cart_quantity
    
    