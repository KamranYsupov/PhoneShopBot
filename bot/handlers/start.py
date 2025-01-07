﻿import loguru
from aiogram import Router, types
from aiogram.filters import CommandStart, Command, CommandObject

from keyboards.reply import reply_start_keyboard
from models import TelegramUser

router = Router()


@router.message(CommandStart())
async def start_command_handler(
    message: types.Message,
    command: CommandObject,
):
    telegram_user_id = command.args if command.args \
        else message.from_user.id
    telegram_user = await TelegramUser.objects.aget(
        id=telegram_user_id
    )
    if (
        (not telegram_user) 
        or 
        (telegram_user.telegram_id and \
        telegram_user.telegram_id != message.from_user.id)
    ):
        
        await message.answer('Неправильная ссылка')
        return             
        
    telegram_user.telegram_id = message.from_user.id
    telegram_user.username = message.from_user.username
    await telegram_user.asave()

    message_text = (
        f'Привет, {telegram_user.fio}.'
    )
    await message.answer(
        message_text,
        reply_markup=reply_start_keyboard
    )
    return 
    
    
    
    
    

    
    

