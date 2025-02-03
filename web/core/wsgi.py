import os

from django.core.wsgi import get_wsgi_application
from django.db.utils. import ProgrammingError

from web.apps.bot_settings.models import BotSettings
    
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

application = get_wsgi_application()

try:
    bot_settings = BotSettings.get_instance()
    bot_settings.is_active = True
    bot_settings.save()
except ProgrammingError
    pass
    

