import asyncio
import os

import django
from django.conf import settings
import loguru
from aiogram.client.default import DefaultBotProperties

from .loader import bot, dp


async def start_bot():
    """Запуск бота"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

    django.setup()
    
    from bot.middlewares.throttling import rate_limit_middleware
    from bot.handlers.routing import get_main_router
    
    dp.message.middleware(rate_limit_middleware)
    dp.include_router(get_main_router())
    loguru.logger.info('Bot is starting')
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
        

if __name__ == '__main__':
    asyncio.run(main())
