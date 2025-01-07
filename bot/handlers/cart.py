import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_inline_keyboard
from models import TelegramUser, Device, CartItem
from utils.message import get_cart_message_and_buttons

router = Router()


@router.callback_query(F.data == 'cart')
async def cart_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await state.clear()
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=callback.from_user.id
    )
    cart_items = await CartItem.objects.afilter(
        telegram_user_id=telegram_user.id,
        select_relations=('device', )
    )
    
    message_text, buttons = get_cart_message_and_buttons(
        cart_items
    )
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1,) * (len(buttons) - 2) + (2, ) 
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data == 'ask_clear_cart')
async def ask_clear_cart_callback_handler(
    callback: types.CallbackQuery,
):  
    buttons = {
        'Да': 'clear_cart',
        'Нет': 'cart',
    }
    
    await callback.message.edit_text(
        '<b>Вы уверены?</b>',
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(2, )
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data == 'clear_cart')
async def clear_cart_callback_handler(
    callback: types.CallbackQuery,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=callback.from_user.id
    )
    cart = await CartItem.objects.filter(
        telegram_user_id=telegram_user.id,
    ).adelete()
        
    await callback.message.edit_text(
        '<b>Корзина успешно очищена ✅</b>',
        reply_markup=get_inline_keyboard(
            buttons={'Вернуться в меню 📁': 'menu'},
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data.startswith('rm_from_cart_'))
async def remove_from_cart_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await state.clear()
    device_id = callback.data.split('_')[-1]
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=callback.from_user.id
    )
    device = await Device.objects.aget(id=device_id)
    
    await CartItem.objects.filter(
        telegram_user_id=telegram_user.id,
        device_id=device.id
    ).adelete()
    
    buttons = {
        'Корзина 🛒': 'cart',
        'Вернуться в меню 📁': 'menu',
    }
    
    await callback.message.edit_text(
        f'<b>{device.name}</b> успешно удален из корзины ✅',
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, 1)
        ),
        parse_mode='HTML',
    )
    