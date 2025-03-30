import asyncio
from datetime import timedelta

from asgiref.sync import async_to_sync
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from web.apps.telegram_users.models import TelegramUser
from web.services.telegram_service import telegram_service


@shared_task(ignore_result=True)
def send_message_task(
        chat_id: str | int,
        text: str,
):
    telegram_service.send_message(chat_id, text)