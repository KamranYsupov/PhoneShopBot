import loguru
from aiogram import Router, types
from aiogram.filters import CommandStart, Command, CommandObject

from keyboards.inline import get_inline_keyboard
from web.apps.telegram_users.models import TelegramUser

router = Router()


@router.message(CommandStart())
async def start_command_handler(
    message: types.Message,
    command: CommandObject,
):
    telegram_user = await TelegramUser.objects.aget(id=command.args)
    if (
        not telegram_user 
        or 
        telegram_user.telegram_id != message.from_user.id
    ):
        await message.answer('Неправильная ссылка')
        return
    
    telegram_user.telegram_id = message.from_user.id
    telegram_user.username = message.from_user.username
    await telegram_user.asave()
    
    buttons = {
        'Посмотреть цены': 'companies',
        'Поиск': 'search',
    }
    await message.answer(
        f'Привет, {telegram_user.fio}',
        reply_markup=get_inline_keyboard(
            buttons=buttons,
        )
    )
    
    
    

    
    

