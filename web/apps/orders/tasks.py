from datetime import date

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from bot.utils.message import get_order_message_and_buttons
from web.services.telegram_service import telegram_service
from web.utils.requests import verify_status_code
from web.apps.telegram_users.models import TelegramUser
from web.apps.orders.models import Order
from web.apps.orders.service import create_order_from_cart


@shared_task(ignore_result=True)
def create_order_from_cart_task(
    telegram_id: TelegramUser.telegram_id,
    comment: str | None = None
):
    """Задача для автоматического создания заказа"""
    order = create_order_from_cart(
        telegram_id=telegram_id,
        comment=comment
    )
    if not order: 
        return 
    order_info_message, buttons = get_order_message_and_buttons(
        order.items.all()
    )
    if not comment:
        comment = 'Без комментария'
        
    message_text = (
        f'Заказ <b>#{order.number}</b> успешно создан!\n\n'
        + order_info_message
        + f'\nКомментарий: <b>{comment}</b>'
    )
    
    telegram_service.send_message(
        chat_id=telegram_id,
        text=message_text,
    )
    response = telegram_service.send_message(
        chat_id=telegram_id,
        text='⏳Пожалуйста, подождите. Ваш заказ оформляется...',
    )

    return verify_status_code(response)



