﻿from datetime import date 

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction

from web.db.model_mixins import (
    AsyncBaseModel,
    QuantityMixin,
)
from web.services.telegram_service import telegram_service


class Order(AsyncBaseModel):
    """Модель заказа"""
    
    class Status:
        ARRIVED = 'ARRIVED'
        BOUGHT = 'BOUGHT'
        CHANGED = 'CHANGED'
        CANCELED = 'CANCELED'
        
        choices = (
            (ARRIVED, _('Прибыл')),
            (BOUGHT, _('Куплен')),
            (CHANGED, _('Изменён')),
            (CANCELED, _('Отменён')),
        )


    number = models.BigIntegerField(_('Номер заказа'))
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=11,
        choices=Status.choices,
        default=Status.ARRIVED,
        db_index=True,
    )
    buyer = models.ForeignKey(
        'telegram_users.TelegramUser', 
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Покупатель'),
    )
    comment = models.CharField(
        _('Комментарий'),
        max_length=150,
        blank=True,
    )
    created_at = models.DateField(
        _('Дата'),
        default=date.today,
        db_index=True,
    )

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')
        ordering = ['-number']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__status = self.status
        
    def save(self, *args, **kwargs):
        if self._state.adding:  # Если объект новый
            # Получаем максимальное значение и увеличиваем его на 1
            max_value = Order.objects.aggregate(
                models.Max('number')
            )['number__max']
            
            self.number = (max_value or 0) + 1  # Увеличиваем на 1, если max_value None
            
            super().save(*args, **kwargs)
            return 
            
        if self.__status == self.status:
            super().save(*args, **kwargs)
            return 
        
        if self.status == Order.Status.CANCELED:
            text = '❌ Заказ отменён'
        elif self.status == Order.Status.BOUGHT:
            text = '✅ Заказ подтвержден'
        elif self.status == Order.Status.CHANGED:
            text = '🟨 Заказ подтвержден частично'

            
        inline_keyboard = [[
            {
                'text': 'Открыть заказ',
                'callback_data': f'order_{self.id}'
            }
        ]]
        telegram_service.send_message(
            chat_id=self.buyer.telegram_id,
            text=text,
            reply_markup={'inline_keyboard': inline_keyboard}
        )   
         
        super().save(*args, **kwargs)
        

    def __str__(self):
        return str(self.number)
    
    
class OrderItem(AsyncBaseModel, QuantityMixin):
    """Модель элемента заказа"""
    general_price = models.PositiveBigIntegerField(
        _('Цена'),
        default=0 
    )

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
        verbose_name = _(' ')
        verbose_name_plural = _('элементы заказа')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__quantity = self.quantity

    def __str__(self):
        return (
            f'{self.device.name} × {self.quantity}'
        )

    def save(self, *args, **kwargs):
        if self._state.adding:  # Если создаем объект
            self.general_price = self.get_general_price() if not self.general_price \
                else self.general_price
            return super().save(*args, **kwargs)

        if self.quantity > (self.__quantity + self.device.quantity):
            return

        self.device.quantity += self.__quantity
        self.device.quantity -= self.quantity
        self.device.save()

        super().save(*args, **kwargs)

    def clean(self):
        if self.quantity > (self.__quantity + self.device.quantity):
            raise ValidationError(
                _(f'Количество {self.device.name} '
                  'превышает количесто товара на складе')
            )

    def get_general_price(self) -> int:
        general_price = self.price_for_one * self.quantity
        return general_price

    @property
    def price_for_one(self) -> int:
        price_for_one = self.device.price_from_1 \
            if self.quantity < 20 else self.device.price_from_20

        return price_for_one


