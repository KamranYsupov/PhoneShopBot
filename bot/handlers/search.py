import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext

from utils.message import get_device_info_message
from orm.cart import get_cart_quantity
from keyboards.inline import get_inline_keyboard
from models import (
    TelegramUser,
    Device, 
    CartItem, 
    Order, 
    OrderItem
)
from .state import CartItemState

router = Router()
        
        
@router.inline_query()
async def search_devices(
    inline_query: types.InlineQuery,
    state: FSMContext,
):
    await state.clear()
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=inline_query.from_user.id
    )
    if not telegram_user:
        return 
    
    offset = int(inline_query.offset) if inline_query.offset else 0
    devices = []
    if inline_query.query:
        devices = await Device.objects.afilter(
            name__iregex=inline_query.query
        )
    else:
        devices = await Device.objects.a_all()
        
    results = []
    for device in devices[offset:50]:
        cart_quantity = await get_cart_quantity(
            device_id=device.id,
            telegram_user_id=telegram_user.id,
        )
        message_text = get_device_info_message(device, cart_quantity)
        message_text += (
            '\nНажмите на кнопку <b><em>"Указать количетсво"</em></b> '
            'и отправьте новое количество устройства в корзине'
        )
        inline_query_result = types.InlineQueryResultArticle(
            id=device.id, 
            title=device.name,
            input_message_content=types.InputTextMessageContent(
                message_text=message_text,
                parse_mode='HTML'
            ),
            reply_markup=get_inline_keyboard(
                buttons={'Указать количетсво': f'q_state_{device.id}'}
            ),
           
        )
        
        results.append(inline_query_result)
        
    if len(results) < 50:
        await inline_query.answer(
            results, 
            cache_time=1,
            is_personal=True
        )
    else:
        await inline_query.answer(
            results, 
            cache_time=1,
            is_personal=True,
            next_offset=str(offset + 50)
        )


@router.callback_query(F.data.startswith('q_state_'))
async def set_quantity_state_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    device_id = callback.data.split('_')[-1]
    
    await state.update_data(device_id=device_id)
    await state.set_state(CartItemState.quantity)