from models import Device, CartItem


def get_device_info_message(
    device: Device,
    cart_quantity: int | None = None
) -> str:
    quantity_string = '100+' if device.quantity > 100 else device.quantity
    
    device_info_message = (
        f'<b>{device.name}</b>\n\n'
        f'<b>Количество:</b> <em>{quantity_string}</em>\n'
    )
    
    if cart_quantity is not None: 
        device_info_message += \
            f'<b>Уже в корзине:</b> <em>{cart_quantity}</em>\n\n'
            
    device_info_message += (
        f'<b>От 1 шт:</b> <em>{device.price_from_1}</em> <b>₽</b>\n'
        f'<b>От 20 шт:</b> <em>{device.price_from_20}</em> <b>₽</b>\n'
    )
    
    return device_info_message


def get_cart_item_info_message(
    cart_item: CartItem,
) -> str:    
    price_for_one_string = get_formated_digit_string(
        cart_item.price_for_one, ' '
    )
    general_price_string = get_formated_digit_string(
        cart_item.general_price, ' '
    ) 
        
    cart_item_info = (
        f'<b>{cart_item.device.name}</b>\n'
        f'<em>◦ <b>{cart_item.quantity} шт</b> × <b>{price_for_one_string}</b>'
        f' = <b>{general_price_string} руб</b></em>'
    )
    
    return cart_item_info
    
    
def get_formated_digit_string(
    digit: int | float,
    format_str: str = '.'
) -> str:
    """1000 -> 1.000"""
    return format(digit, ',').replace(',', format_str) 
    
    