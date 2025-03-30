import os

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel, SingletonModel,
)


class BotSettings(AsyncBaseModel):
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Bot is {'active' if self.is_active else 'inactive'}"
    
    @classmethod
    def get_instance(cls):
        instance = cls.objects.first() 
        if not instance:
            instance = cls(pk=1)
            instance.save()
            
        return instance


    def save(self, *args, **kwargs):
        if self._state.adding:
            if BotSettings.objects.exists():
                raise ValueError("Only one instance of BotSettings can exist.")
        super().save(*args, **kwargs)


class Settings(SingletonModel):
    orders_receiver_telegram_id = models.BigIntegerField(
        verbose_name='Телеграм ID',
        default=settings.ANALYTIC_RECEIVER_TELEGRAM_ID
    )

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Настройки'