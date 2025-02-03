import loguru
from aiogram import Router, types, F
from aiogram.filters import StateFilter, CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import (
    get_inline_keyboard,
    get_inline_menu_keyboard
)
from bot.keyboards.reply import reply_start_keyboard
from bot.models import TelegramUser

router = Router()

@router.message(F.text.casefold() == 'меню 📁')
@router.callback_query(F.data == 'menu')
async def menu_handler(
    tg_obj: types.Message | types.CallbackQuery,
    state: FSMContext,
):
    await state.clear()
    if isinstance(tg_obj, types.Message):
        message_method = tg_obj.answer
    else: 
        message_method = tg_obj.message.edit_text
        
    await message_method(
        'Выберите пункт меню.',
        reply_markup=get_inline_menu_keyboard()
    )
    
    
@router.callback_query(F.data == 'faq')
async def faq_callback_handler(callback: types.CallbackQuery):
    with open('FAQ.txt', 'r', encoding='utf-8') as file:
        message_text = file.read()
        
    await callback.message.edit_text(
        text=message_text,
        reply_markup=get_inline_keyboard(
            buttons={'Назад 🔙': 'menu'}, 
        ),
    )
    
    
@router.message(
    StateFilter('*'),
    (F.text == 'Отмена ❌')
)
async def cancel_callback_handler(
    message: types.Message,
    state: FSMContext,
):
    await state.clear()
    await message.answer(
        'Действие отменено',
        reply_markup=reply_start_keyboard,
    )
    
    