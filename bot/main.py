import asyncio
import os

import django
from django.conf import settings
import loguru
from aiogram.client.default import DefaultBotProperties

from bot.loader import bot, dp


async def main():
    """Запуск бота"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

    django.setup()
    
    from bot.middlewares.throttling import (
        rate_limit_middleware,
        is_bot_active_middleware,
    )
    from bot.handlers.routing import get_main_router
    
    dp.message.middleware(is_bot_active_middleware)
    dp.message.middleware(rate_limit_middleware)
    dp.include_router(get_main_router())
    
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        

if __name__ == '__main__':
    loguru.logger.info('Bot is starting')
    asyncio.run(main())
