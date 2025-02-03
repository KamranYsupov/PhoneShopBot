import threading
import asyncio

import asyncio

from bot.main import start_bot
from bot.loader import bot
from web.apps.bot_settings.models import BotSettings

def sync_start_bot():
    asyncio.run(start_bot())
 
def sync_stop_bot():
    asyncio.run(bot.session.close())
    
def change_bot_status() -> None:   
    """Функция, которая включает/выключает бота при вызове"""
    bot_settings = BotSettings.get_instance()
    
    if bot_settings.is_active:
        bot_settings.is_active = False
        target_func = sync_start_bot
        print('start')
    else:
        bot_settings.is_active = True
        target_func = sync_stop_bot
        print('stop')
    
    
    bot_settings.save()    
    thread = threading.Thread(target=target_func)
    thread.start()            

    
    