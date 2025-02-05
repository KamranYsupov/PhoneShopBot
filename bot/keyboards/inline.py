from typing import Dict, Tuple

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from django.conf import settings

from bot.models import Device

def get_inline_keyboard(*, buttons: Dict[str, str], sizes: Tuple = (1, 2)):
    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


def get_inline_menu_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text='Посмотреть цены 🗂',
            callback_data='companies_1'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Корзина 🛒',
            callback_data='cart_1'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Мои заказы 📦',
            callback_data='my_orders_1'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Поиск модели 🔎',
            switch_inline_query_current_chat=''
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Выгрузка в Excel ⬇️',
            callback_data='excel_devices'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='FAQ ❓',
            callback_data='faq'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Связатся с менеджером ☎️',
            url=settings.MANAGER_ACCOUNT_LINK,
        )
    )
    
    return keyboard.adjust(1, 2, 1, 1, 1, 1).as_markup()

    
inline_cancel_keyboard = get_inline_keyboard(
    buttons={'Отмена ❌': 'cancel'}
)