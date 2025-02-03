import os

from django.core.wsgi import get_wsgi_application

from web.apps.bot_settings.models import BotSettings
    
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

application = get_wsgi_application()

bot_settings = BotSettings.get_instance()
bot_settings.is_active = False
bot_settings.save()
