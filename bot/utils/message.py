from typing import Sequence, Union
from collections import defaultdict

from asgiref.sync import sync_to_async

from bot.models import (
    TelegramUser,
    Device,
    DeviceCompany,
    DeviceModel,
    DeviceSeries, 
    CartItem, 
    Order, 
    OrderItem
)
from bot.utils.sort import sort_objects_by_parent


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
    is_cart: bool = True,
    start_index: int = 1,
) -> tuple[str, dict]:
    buttons = {}
    message_text = ''
    total_price = 0
    
    index = start_index
    for item in items:
        total_price += item.general_price
        message_text += f'{index}) {get_item_info_message(item)}\n\n'
        
        if is_cart:
            buttons[item.device.name] = f'dev_{item.device_id}_1_1'
            
        index += 1
            
    total_price_label = f'Итого: <b>{total_price} $</b>'
    
    if is_cart:
        if not message_text:
            message_text = 'Ваша корзина пуста.' 
        else:
            message_text = (
                f'<b>Корзина:</b>\n\n{message_text}'
                + total_price_label
            )
    else:
        message_text += total_price_label
        buttons['Корзина 🛒'] = 'cart_1'

    return message_text, buttons


def get_cart_message_and_buttons(
    cart_items: Sequence[CartItem],
    start_index: int = 1,
) -> tuple[str, dict]:
    return get_message_and_buttons(
        cart_items, 
        is_cart=True,
        start_index=start_index,
    )


def get_order_message_and_buttons(
    order_items: Sequence[OrderItem],
    start_index: int = 1,
) -> tuple[str, dict]:
    message_text, buttons = get_message_and_buttons(
        order_items, 
        is_cart=False,
        start_index=start_index,
    )
    buttons['Вернуться в меню 📁'] = 'menu'
    
    return message_text, buttons
    
    
@sync_to_async
def get_order_items_info_message(orders: Sequence) -> str:
    """Функция для формирования строки содержащей информацию о заказах"""
    order_items_data = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(lambda: defaultdict(list))
        )
    )
    order_items = OrderItem.objects.filter(
        order_id__in=[order.id for order in orders]
    ).select_related( 
        'device__series__model',
        'device__series',
        'device'
    )
    
    companies_ids = set()
    for item in order_items:
        company_id = item.device.series.model.company_id
        model = item.device.series.model
        series = item.device.series
        device = item.device

        order_items_data[company_id][model][series][device].append(item)
        companies_ids.add(company_id)

    sorted_order_items_data = {}

    companies = DeviceCompany.objects.filter(id__in=companies_ids)
    models = DeviceModel.objects.filter(company_id__in=companies_ids)
    series = DeviceSeries.objects.filter(
        model_id__in=[model.id for model in models]
    )
    devices = Device.objects.filter(
        series_id__in=[series_obj.id for series_obj in series]
    )
    items = OrderItem.objects.filter(
        device_id__in=[device.id for device in devices]
    )
    
    models_by_company_id = defaultdict(list) 
    series_by_models_id = defaultdict(list) 
    devices_by_series_id = defaultdict(list) 
    items_by_series_id = defaultdict(list) 
    
    for model in models:
        models_by_company_id[model.company_id].append(model)
        
    for series_obj in series:
        series_by_models_id[series_obj.model_id].append(series_obj)
        
    for device in devices:
        devices_by_series_id[device.series_id].append(device)

    for item in items:
        items_by_series_id[item.device_id].append(item)
        
    for company in companies:
        sorted_order_items_data[company] = {}
        
        sorted_models = sort_objects_by_parent(
            related_manager_objects=models_by_company_id[company.id], 
            objects=order_items_data[company.id]
        )
        for model in sorted_models:
            sorted_order_items_data[company][model] = {}

            sorted_series = sort_objects_by_parent(
                related_manager_objects=series_by_models_id[model.id], 
                objects=order_items_data[company.id][model]
            )
            for series in sorted_series:
                sorted_order_items_data[company][model][series] = {}
                
                sorted_devices = sort_objects_by_parent(
                    related_manager_objects=devices_by_series_id[series.id], 
                    objects=order_items_data[company.id][model][series]
                )
                for device in sorted_devices:
                    sorted_order_items_data[company][model][series][device] = []
                    
                    sorted_items = sort_objects_by_parent(
                        related_manager_objects=items_by_series_id[device.id], 
                        objects=order_items_data[company.id][model][series][device]
                    ) 
                    
                    for item in sorted_items:
                        sorted_order_items_data[company][model][series][device].append(item)
    
    message_text = ''
    total_orders_price = 0
              
    count = 1  
    for company in sorted_order_items_data:
        for model in sorted_order_items_data[company]:
            for series in sorted_order_items_data[company][model]:
                for device in sorted_order_items_data[company][model][series]:
                    items = sorted_order_items_data[company][model][series][device] 
                    message_text += f'{count}) <b>{items[0].device.name}</b>\n'
                        
                    for item in items:
                        message_text += ''.join(
                            get_item_info_message(item)
                            .split('\n')[1:]
                        ) # Убираем первую строчку
                    
                        message_text += '\n\n'
                            
                    total_orders_price += item.general_price
                    count += 1
        
    message_text += f'Общая сумма: <b>{total_orders_price} $</b>'
    
    return message_text


def get_formated_digit_string(
    digit: int | float,
    format_str: str = '.'
) -> str:
    """1000 -> 1.000"""
    return format(digit, ',').replace(',', format_str) 
