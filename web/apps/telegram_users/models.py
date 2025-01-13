from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
    AbstractTelegramUser,
    QuantityMixin
)


class TelegramUser(AbstractTelegramUser):
    """Модель telegram пользователя"""
    fio = models.CharField(
        _('ФИО'),
        max_length=150
    )
    phone_number = models.CharField(
        _('Номер телефона'),
        max_length=50,
        unique=True,
    )
    bot_start_link = models.CharField(
        _('Ссылка для запуска бота'),
        max_length=150,
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('Telegram пользователи')

    def __str__(self):
        return f'{self.fio} {self.phone_number}'
    
    def save(self, *args, **kwargs):
        if self._state.adding: # Если создаем объект 
            self.bot_start_link = f'{settings.BOT_LINK}?start={self.id}'
            
        return super().save(*args, **kwargs)
        

class CartItem(AsyncBaseModel, QuantityMixin):
    """Модель элемента корзины"""
    telegram_user = models.ForeignKey(
        'telegram_users.TelegramUser', 
        on_delete=models.CASCADE,
        related_name='cart'
    )
    device = models.ForeignKey(
        'devices.Device', 
        on_delete=models.CASCADE,
        verbose_name=_('Устройство')
    )
    
    class Meta:
        verbose_name = _('элемент корзины')
        verbose_name_plural = _('корзина')
        
    @property
    def general_price(self) -> int:
        general_price = self.price_for_one
        
        return general_price * self.quantity
       
    @property 
    def price_for_one(self) -> int:
        price_for_one = self.device.price_from_1 \
            if self.quantity < 20 else self.device.price_from_20
        
        return price_for_one   