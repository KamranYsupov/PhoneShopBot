from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings

from .models import Notification
from web.services.telegram_service import telegram_service
    
    
@receiver(post_save, sender=Notification)
def send_notification_after_creation(sender, instance: Notification, created, **kwargs):
    if not created:
        return

    def send_notification():
        for receiver in instance.receivers.all():
            text = instance.text if instance.text else instance.template.text
            telegram_service.send_message(
                chat_id=receiver.telegram_id,
                text=text
            )

    transaction.on_commit(send_notification)
