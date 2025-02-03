from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings

from .models import Order, OrderItem
from web.apps.devices.models import Device
from web.services.telegram_service import telegram_service



@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):     
    if created:   
        return 
    if instance.status == Order.Status.CANCELED:
        text = (
            'К сожалению данной позиции нет в наличии, '
            'если готовы приобрести по более высокой цене, '
            'обратитесь к менеджеру'
        )
        inline_keyboard = [[
        {
            'text': 'Открыть заказ',
            'callback_data': f'order_{instance.id}'
        }
    ]]
         
    
        telegram_service.send_message(
        chat_id=instance.buyer.telegram_id,
        text=text,
        reply_markup={'inline_keyboard': inline_keyboard}
    )
            

@receiver(post_delete, sender=Order)
def order_post_delete(sender, instance, **kwargs):
    items_ids = []
    
    with transaction.atomic():
        for item in instance.items.select_related('device'):
            items_ids.append(item.id)
        
        OrderItem.objects.filter(id__in=items_ids).delete()
        
        
@receiver(post_delete, sender=OrderItem)
def order_item_post_delete(sender, instance, **kwargs):
    instance.device.quantity += instance.quantity
    instance.device.save()
    