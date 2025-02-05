from datetime import timedelta
import uuid

from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings

from .models import TelegramUser, CartItem
from web.apps.orders.tasks import create_order_from_cart_task
from web.core.celery import is_task_with_params_running


@receiver(post_save, sender=CartItem)
def post_save_cart_item(sender, instance, created, **kwargs):
    if not created:
       return
     
    task_args = [instance.telegram_user.telegram_id]
    if not is_task_with_params_running(task_args):
        now = timezone.now()
        create_order_from_cart_task.apply_async(
            args=task_args,
            eta=now + timedelta(minutes=settings.ORDER_AUTO_CREATE_MINUTES_INTERVAL)
        )
            
 