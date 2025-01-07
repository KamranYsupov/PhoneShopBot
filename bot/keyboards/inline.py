﻿from typing import Dict, Tuple

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


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
        'Мои заказы': 'my_orders',
        'FAQ': 'faq',
        'Связаться с менеджером': 'manager',
    }
)