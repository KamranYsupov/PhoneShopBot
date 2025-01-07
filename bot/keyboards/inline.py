from typing import Dict, Tuple

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from models import Device

def get_inline_keyboard(*, buttons: Dict[str, str], sizes: Tuple = (1, 2)):
    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


inline_cancel_keyboard = get_inline_keyboard(
    buttons={'Отмена ❌': 'cancel'}
)
inline_menu_keyboard = get_inline_keyboard(
    buttons={
        'Посмотреть цены': 'companies_1',
        'Поиск': 'search',
        'Корзина': 'cart',
        'Мои заказы': 'my_orders_1',
        'FAQ': 'faq',
        'Связаться с менеджером': 'manager',
    }
)


def get_device_inline_keyboard(device_id: Device.id):
    buttons = {
        'Убрать из корзины 🗑': f'rm_from_cart_{device_id}',
        'Корзина 🛒': 'cart',
        'Вернуться в меню 📁': 'menu',
    }
    
    return get_inline_keyboard(
        buttons=buttons,
        sizes=(1, 1, 1)
    )