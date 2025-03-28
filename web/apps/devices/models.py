﻿from django.db import models
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
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'company'],
                name='unique_model_name_per_company'
            )
        ]

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
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'model'],
                name='unique_series_name_per_model'
            )
        ]

    def __str__(self):
        return self.name
    
    
class Device(AsyncBaseModel, QuantityMixin):
    """Модель устройства"""
    name = models.CharField(
        _('Название'),
        max_length=200,
        db_index=True,
    )
    price_from_1 = models.PositiveBigIntegerField(_('Цена от 1 шт'))
    price_from_20 = models.PositiveBigIntegerField(_('Цена от 20 шт'))
    
    series = models.ForeignKey(
        'devices.DeviceSeries',
        verbose_name=_('Серия'), 
        on_delete=models.CASCADE,
        related_name='devices'
    )
    supplier = models.ForeignKey(
        'devices.Supplier',
        verbose_name=_('Поставщик'), 
        on_delete=models.SET_NULL,
        related_name='devices',
        null=True,
    )
    
    class Meta:
        verbose_name = _('устройство')
        verbose_name_plural = _('устройства')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'series'],
                name='unique_device_name_per_series'
            )
        ]

    def __str__(self):
        return self.name


class Supplier(AsyncBaseModel):
    """Модель поставщика"""
    name = models.CharField(
        _('Имя'),
        max_length=200,
        db_index=True,
    )
    
    class Meta:
        verbose_name = _('поставщик')
        verbose_name_plural = _('поставщики')

    def __str__(self):
        return self.name


