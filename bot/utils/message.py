from typing import Sequence, Union

from models import Device, CartItem, OrderItem


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
        f'<b>От 1 шт:</b> <em>{device.price_from_1}</em> <b>$</b>\n'
        f'<b>От 20 шт:</b> <em>{device.price_from_20}</em> <b>$</b>\n'
    )
    
    return device_info_message


def get_item_info_message(item: CartItem | OrderItem) -> str:
    price_for_one_string = get_formated_digit_string(item.price_for_one, ' ')
    general_price_string = get_formated_digit_string(item.general_price, ' ')
    
    if isinstance(item, CartItem):
        format_tag = 'em'
    else:
        format_tag = 'blockquote'
        
    return (
        f'<b>{item.device.name}</b>\n'
        f'<{format_tag}>◦ <b>{item.quantity} шт</b> × <b>{price_for_one_string}</b>'
        f' = <b>{general_price_string} $</b></{format_tag}>'
    )


def get_message_and_buttons(
    items: Sequence[Union[CartItem, OrderItem]], 
    is_cart: bool = True
) -> tuple[str, dict]:
    buttons = {}
    message_text = ''
    total_price = 0
    
    for index, item in enumerate(items):
        total_price += item.general_price
        message_text += f'{index + 1}) {get_item_info_message(item)}\n\n'
        
        if is_cart:
            buttons[item.device.name] = f'dev_{item.device_id}_1_1'
            
    total_price_label = f'Итого: <b>{total_price} $</b>'
    
    if is_cart:
        if not message_text:
            message_text = 'Ваша корзина пуста.' 
        else:
            message_text = (
                f'<b>Корзина:</b>\n\n{message_text}'
                + total_price_label
            )
            buttons.update({
                'Создать заказ 📝': 'create_order',
                'Очистить корзину 🧹': 'ask_clear_cart',
            })
    else:
        message_text += total_price_label
        buttons['Корзина 🛒'] = 'cart'
    
    
    buttons['Вернуться в меню 📁'] = 'menu'
    
    return message_text, buttons


def get_cart_message_and_buttons(
    cart_items: Sequence[CartItem]
) -> tuple[str, dict]:
    return get_message_and_buttons(
        cart_items, 
        is_cart=True
    )


def get_order_message_and_buttons(
    order_items: Sequence[OrderItem]
) -> tuple[str, dict]:
    return get_message_and_buttons(
        order_items, 
        is_cart=False
    )
    
def get_formated_digit_string(
    digit: int | float,
    format_str: str = '.'
) -> str:
    """1000 -> 1.000"""
    return format(digit, ',').replace(',', format_str) 
    
    