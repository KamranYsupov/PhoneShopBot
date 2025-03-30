from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import AsyncBaseModel


class TelegramMessageModelMixin(models.Model):
    """Миксин для телеграм сообщения"""
    name = models.CharField(
        _('Название(опционально)'),
        max_length=150,
        null=True,
        blank=True,
        default=None,
    )
    text = models.TextField(
        _('Текст'),
        max_length=4000,
    )
    created_at = models.DateTimeField(
        _('Время и дата создания'),
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
        
    def __str__(self):
        if self.name:
            return self.name
        
        return self.get_short_text()
    
    def get_short_text(self):
        if len(self.text) > 150:
            return f'{self.text[:150]}...'
        
        return self.text
    

class NotificationTemplate(AsyncBaseModel, TelegramMessageModelMixin):
    """Модель шаблона рассылки"""

    class Meta:
        verbose_name = _('Шаблон рассылки')
        verbose_name_plural = _('Шаблоны рассылки')


class Notification(AsyncBaseModel, TelegramMessageModelMixin):
    """Модель telegram уведомления"""
    text = models.TextField(
        _('Текст'),
        max_length=4000,
        null=True,
        blank=True,
        default=None,
    )
    template = models.ForeignKey(
        'notifications.NotificationTemplate',
        verbose_name=_('Шаблон'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    receivers = models.ManyToManyField(
        'telegram_users.TelegramUser', 
        verbose_name=_('Получатели')
    )
    
    class Meta:
        verbose_name = _('Уведомление')
        verbose_name_plural = _('Уведомления')

    def clean(self):
        if not self.text and not self.template:
            raise ValidationError(
                'Одно из полей "Текст", или "Шаблон" должно быть заполнено'
            )