import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from asgiref.sync import sync_to_async

from keyboards.inline import get_inline_keyboard
from keyboards.reply import (
    get_reply_keyboard,
    reply_keyboard_remove,
    reply_cancel_keyboard
)
from .state import OrderState
from orm.orders import create_order
from models import (
    TelegramUser,
    Device, 
    CartItem, 
    Order, 
    OrderItem
)
from utils.bot import edit_text_or_answer
from utils.message import get_order_message_and_buttons

router = Router()


@router.callback_query(F.data == 'create_order')
async def create_order_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await state.set_state(OrderState.comment)
    
    await callback.message.delete()
    await callback.message.answer(
        'Укажите комментарий',
        reply_markup=get_inline_keyboard(
            buttons={'Пропустить ➡️': 'complete_create_order'}
        )
    )
    
    
@router.callback_query(F.data == 'complete_create_order')
async def complete_create_order_callback_handler(
    callback: types.CallbackQuery,
):
    await complete_create_order_handler(
        message=callback.message,
        telegram_id=callback.from_user.id,
    )
    

@router.message(F.text, OrderState.comment)
async def complete_create_order_message_handler(
    message: types.Message,
):
    await complete_create_order_handler(
        message=message,
        telegram_id=message.from_user.id,
        comment=message.text
    )
    
    
async def complete_create_order_handler(
    message: types.Message,
    telegram_id: int,
    comment: str | None = None,
):
    create_order_data = {'telegram_id': telegram_id}
    
    if comment:
        create_order_data['comment'] = comment
    else:
        comment = 'Без комментария'
        
    result = await create_order(**create_order_data)
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

    await edit_text_or_answer(
        message,
        text=message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, 1)
        ),
        parse_mode='HTML'
    )
        

        
    
        
        
        
        
        