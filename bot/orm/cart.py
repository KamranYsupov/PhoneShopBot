from asgiref.sync import sync_to_async

from models import (
    TelegramUser, 
    CartItem,
    Device
)
from utils.validators import validate_quantity

from typing import Any

@sync_to_async
async def add_to_cart(
    device_id: Device.id,
    telegram_user_id: TelegramUser.id, 
    quantity: Any,
) -> CartItem | None:
    device = await Device.objects.aget(id=device_id)
    quantity = await validate_quantity(
        message, 
        device.quantity,
        quantity,
    )
    if not quantity:
        return
    
    cart_item, created = await CartItem.objects.aget_or_create(
        device_id=device_id,
        telegram_user_id=telegram_user_id,
        defaults={'quantity': quantity}  
    )

    if not created:
        cart_item.quantity = quantity 
        await cart_item.asave()  

    return cart_item
    
    
    