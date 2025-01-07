from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction

from web.db.model_mixins import (
    AsyncBaseModel,
    QuantityMixin,
)


class Order(AsyncBaseModel):
    """Модель заказа"""
    
    class Status:
        ARRIVED = 'ARRIVED'
        BOUGHT = 'BOUGHT'
        ASSEMBLED = 'ASSEMBLED'
        КNOCKED_OUT = 'КNOCKED_OUT'
        CANCEL = 'CANCEL'
        
        choices = (
            (ARRIVED, _('Прибыл')),
            (BOUGHT, _('Куплен')),
            (ASSEMBLED, _('Собран')),
            (КNOCKED_OUT, _('Выбит')),
            (CANCEL, _('Отменён')),
        )


    number = models.BigIntegerField(_('Номер заказа'))
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=11,
        choices=Status.choices,
        default=Status.ARRIVED,
    )
    buyer = models.ForeignKey(
        'telegram_users.TelegramUser', 
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Покупатель'),
    )

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')
        
    def save(self, *args, **kwargs):
        if self._state.adding:  # Если объект новый
            # Получаем максимальное значение и увеличиваем его на 1
            max_value = Order.objects.aggregate(
                models.Max('number')
            )['number__max']
            
            self.number = (max_value or 0) + 1  # Увеличиваем на 1, если max_value None
            
        super.save(**args, **kwargs)
            
    def clean(self):
        super().clean()
        if not self.items.all():
            raise ValidationError(
                'В заказ должен быть добавлен хотя бы 1 элемент'
            )

    def __str__(self):
        return str(self.number)
    
    
class OrderItem(AsyncBaseModel, QuantityMixin):
    """Модель элемента заказа"""
    order = models.ForeignKey(
        'orders.Order', 
        on_delete=models.CASCADE,
        related_name='items'
    )
    device = models.ForeignKey(
        'devices.Device', 
        on_delete=models.CASCADE,
        verbose_name=_('Устройство'),
    )
    
    class Meta:
        verbose_name = _('элемент заказа')
        verbose_name_plural = _('элементы заказа')
    
    


