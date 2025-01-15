import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext

from keyboards.inline import get_inline_keyboard
from models import TelegramUser, Device, CartItem
from utils.message import get_cart_item_info_message

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
    cart = await CartItem.objects.afilter(
        telegram_user_id=telegram_user.id,
        select_relations=('device', )
    )
    
    buttons = {}
    
    cart_data = {}
    for cart_item in cart:
        cart_data[cart_item.device.id] = cart_item
        
    message_text = ''
    cart_price = 0
    for index, device_id in enumerate(cart_data):
        cart_item = cart_data[device_id]
        cart_price += cart_item.general_price
        
        message_text += \
            f'{index + 1}) {get_cart_item_info_message(cart_item)}\n\n'
            
        buttons[cart_item.device.name] = f'dev_{cart_item.device_id}_1_1'
        
    if not message_text:
        message_text += 'Ваша корзина пуста.'
    else: 
        message_text = (
            '<b>Корзина:</b>\n\n' + 
            message_text +
            f'Итого: <b>{cart_price} руб</b>'
        )
        buttons.update({
            'Создать заказ 📝': 'create_order',
            'Очистить корзину 🧹': 'ask_clear_cart',
        })
        
    buttons['Вернуться в меню 📁'] = 'menu'
    
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
    