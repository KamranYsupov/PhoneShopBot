import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from keyboards.inline import get_inline_keyboard
from orm.orders import create_order
from models import (
    TelegramUser,
    Device, 
    CartItem, 
    Order, 
    OrderItem
)
from utils.message import get_order_message_and_buttons

router = Router()


@router.callback_query(F.data == 'create_order')
async def create_order_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    result = await create_order(telegram_id=callback.from_user.id)
    buttons = {
        'Корзина 🛒': 'cart',
        'Вернуться в меню 📁': 'menu'
    }
    
    if isinstance(result, Order):
        order = result
        order_items = await OrderItem.objects.afilter(
            order_id=order.id,
            select_relations=('device', )
        )        
        order_info_message, buttons = get_order_message_and_buttons(
            order_items
        )
        comment = order.comment if order.comment else 'Без комментария'
        message_text = (
            f'Заказ <b>#{order.number}</b> успешно создан!\n\n'
            + order_info_message
            + f'\nКомментарий: <b>{comment}</b>'
        )
        
    elif isinstance(result, list):
        cart_items = result
        cart_items_names = [
            f'<b>{cart_item.device.name}</b>' for cart_item in cart_items
        ]
        message_text = (
            f'Количество устройств {", ".join(cart_items_names)} ' 
            'превышает количество на складе'
        )
    else:
        return
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, 1)
        ),
        parse_mode='HTML'
    )

        
    
        
        
        
        
        