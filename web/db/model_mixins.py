from typing import Sequence, List, Dict

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from ulid import ULID

from .base_manager import AsyncBaseManager
        
        
def ulid_default() -> str:
    return str(ULID())
        
        
class AsyncBaseModel(models.Model):
    id = models.CharField( 
        primary_key=True,
        default=ulid_default,
        max_length=26,
        editable=False,
        unique=True,
        db_index=True,
    )
    
    objects = AsyncBaseManager()
    
    class Meta: 
        abstract = True
        
        
class AbstractTelegramUser(AsyncBaseModel):
    telegram_id = models.BigIntegerField(
        verbose_name=_('Телеграм ID'),
        unique=True,
        db_index=True,
        null=True,
        default=None,

    )
    username = models.CharField(
        _('Имя пользователя'),
        max_length=70,
        unique=True,
        db_index=True,
        null=True,
        default=None,
    )
    
    class Meta: 
        abstract = True
    
    
class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Дата последнего обновления'),
        auto_now=True
    )

    class Meta:
        abstract = True
    
    
class QuantityMixin(models.Model):
    quantity = models.PositiveBigIntegerField(
        verbose_name=_('Количество')
    )

    class Meta:
        abstract = True


class ArchiveMixin(models.Model):
    """Миксин для создания модели с возможностью архивации(скрытия) объектов"""

    is_archived = models.BooleanField(default=False, db_index=False)

    class Meta:
        abstract = True