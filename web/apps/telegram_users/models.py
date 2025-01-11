from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
    AbstractTelegramUser
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
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return f'{self.fio} {self.id}'
    
    def save(self, *args, **kwargs):
        if self._state.adding: # Если создаем объект 
            self.bot_start_link = f'{settings.BOT_LINK}?start={self.id}'
            
        return super().save(*args, **kwargs)
        

class Cart:
    telegram_user = models.ForeignKey(
        TelegramUser, 
        on_delete=models.CASCADE,
        related_name='cart'
    )
    phone_product = models.ForeignKey(
        'phones.PhoneProduct', 
        on_delete=models.CASCADE,
        related_name='cart'
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name=_('Количество')
    )