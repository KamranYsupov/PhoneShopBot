from django.contrib import admin
from django.urls import path, include
from django.db.utils import OperationalError

from web.apps.bot_settings.models import BotSettings

try:
    is_bot_active = BotSettings.get_instance().is_active
except OperationalError:
    is_bot_active = False
    
urlpatterns = [
    path('admin/', admin.site.urls, {
            'extra_context': {'bot_is_active': is_bot_active}
        }),
    path('devices/', include('web.apps.devices.urls')),
    path('bot/', include('web.apps.bot_settings.urls'))
]
