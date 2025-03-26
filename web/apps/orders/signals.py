from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings

from .models import Order, OrderItem
from web.apps.devices.models import Device
from web.services.telegram_service import telegram_service


@receiver(post_delete, sender=Order)
def order_post_delete(sender, instance, **kwargs):
    items_ids = []
    
    with transaction.atomic():
        for item in instance.items.select_related('device'):
            items_ids.append(item.id)
        
        OrderItem.objects.filter(id__in=items_ids).delete()
        
        
@receiver(post_delete, sender=OrderItem)
def order_item_post_delete(sender, instance, **kwargs):
    try:
        instance.device.quantity += instance.quantity
        instance.device.save()
    except AttributeError:
        pass
