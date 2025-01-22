from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator

from web.db.model_mixins import (
    AsyncBaseModel,
    QuantityMixin,
)

class DeviceCompany(AsyncBaseModel):
    """Модель компании устройства"""
    name = models.CharField(
        _('Название'),
        max_length=100,
        unique=True,
        db_index=True,
    )
    
    class Meta:
        verbose_name = _('компания')
        verbose_name_plural = _('компании')

    def __str__(self):
        return self.name
    
    
class DeviceModel(AsyncBaseModel):
    """Модель модели устройства"""
    name = models.CharField(
        _('Название'),
        max_length=100,
        db_index=True,
    )
    
    company = models.ForeignKey(
        'devices.DeviceCompany',
        verbose_name=_('Компания'), 
        on_delete=models.CASCADE,
        related_name='models'
    )
    
    class Meta:
        verbose_name = _('модель')
        verbose_name_plural = _('модели')

    def __str__(self):
        return self.name
    
    
class DeviceSeries(AsyncBaseModel):
    """Модель серии модели устройства"""
    name = models.CharField(
        _('Название'),
        max_length=100,
        db_index=True,
    )
    
    model = models.ForeignKey(
        'devices.DeviceModel',
        verbose_name=_('Модель'), 
        on_delete=models.CASCADE,
        related_name='series'
    )
    
    class Meta:
        verbose_name = _('серия')
        verbose_name_plural = _('серии')

    def __str__(self):
        return self.name
    
    
class Device(AsyncBaseModel, QuantityMixin):
    """Модель устройства"""
    name = models.CharField(
        _('Название'),
        max_length=200,
        db_index=True,
    )
    price_from_1 = models.FloatField(
        _('Цена от 1 шт'),
        validators=[MinValueValidator(0.0)]
    )
    price_from_20 = models.FloatField(
        _('Цена от 20 шт'),
        validators=[MinValueValidator(0.0)]
    )
    
    series = models.ForeignKey(
        'devices.DeviceSeries',
        verbose_name=_('Серия'), 
        on_delete=models.CASCADE,
        related_name='devices'
    )
    
    class Meta:
        verbose_name = _('устройство')
        verbose_name_plural = _('устройства')

    def __str__(self):
        return self.name



