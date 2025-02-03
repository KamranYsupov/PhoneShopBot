import time
from typing import Dict, Callable, Union

from loguru import logger
from aiogram.types import Message, CallbackQuery
from django.conf import settings
from asgiref.sync import sync_to_async

from bot.models import BotSettings    

async def is_bot_active_middleware(
    handler: Callable,
    event: Union[Message, CallbackQuery],
    data: Dict
):
    """
    Middleware для проверки статуса бота.
    Если выключен, то вернет None.
    """
    bot_settings = await sync_to_async(BotSettings.get_instance)()
    
    if not bot_settings.is_active:
        return None  
        
    return await handler(event, data)


async def rate_limit_middleware(
    handler: Callable,
    event: Message,
    data: Dict
):
    """Middleware для ограничения отправки сообщений пользователем боту."""

    user_id = event.from_user.id
    current_time = time.time()

    if not hasattr(rate_limit_middleware, 'users'):
        rate_limit_middleware.users = {}

    if user_id not in rate_limit_middleware.users:
        rate_limit_middleware.users[user_id] = {
            'last_message_time': current_time,
            'warning_sent': False
        }
        return await handler(event, data)

    user_data = rate_limit_middleware.users[user_id]
    last_message_time = user_data['last_message_time']

    if current_time - last_message_time < settings.MAX_MESSAGE_PER_SECOND:
        if not user_data['warning_sent']:
            await event.answer('Слишком много сообщений! Попробуйте позже.')
            user_data['warning_sent'] = True 
        return  

    user_data['last_message_time'] = current_time
    user_data['warning_sent'] = False  
    return await handler(event, data)