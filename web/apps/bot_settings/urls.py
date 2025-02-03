from django.urls import path
from .views import change_bot_status_view

urlpatterns = [
    path('change-bot-status/', change_bot_status_view, name='change_bot_status'),
]