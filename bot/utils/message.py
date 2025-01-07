from models import Device


def get_device_info_message(device: Device) -> str:
    quantity_string = '100+' if device.quantity > 100 else device.quantity
    cart_quantity = 0
    
    device_info_message = (
        f'<b>{device.name}</b>\n\n'
        f'<b>Количество:</b> <em>{quantity_string}</em>\n'
        f'<b>Уже в корзине:</b> <em>{cart_quantity}</em>\n\n'
        f'<b>От 1 шт:</b> <em>{device.price_from_1}</em> <b>₽</b>\n'
        f'<b>От 20 шт:</b> <em>{device.price_from_20}</em> <b>₽</b>\n'
    )
    
    return device_info_message
    