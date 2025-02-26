from django.urls import path
from web.apps.bot_settings.views import change_bot_status_view

urlpatterns = [
    path('change-bot-status/', change_bot_status_view, name='change_bot_status'),
]