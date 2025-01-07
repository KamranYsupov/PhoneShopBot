from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import AsyncBaseModel


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
    devices = models.JSONField(_('Устройства'), default=list)
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=11,
        choices=Status.choices,
        default=Status.ARRIVED,
    )

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        
    def save(self, *args, **kwargs):
        if self._state.adding:  # Если объект новый
            # Получаем максимальное значение и увеличиваем его на 1
            max_value = Order.objects.aggregate(
                models.Max('number')
            )['number__max']
            
            self.number = (max_value or 0) + 1  # Увеличиваем на 1, если max_value None
            
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.number)
    
    


