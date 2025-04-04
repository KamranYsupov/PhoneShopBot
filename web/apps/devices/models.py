from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator

from web.db.model_mixins import (
    ArchiveMixin,
    AsyncBaseModel,
    QuantityMixin,
)

class DeviceCompany(ArchiveMixin, AsyncBaseModel):
    """Модель компании устройства"""
    name = models.CharField(
        _('Название'),
        max_length=100,
        db_index=True,
    )
    
    class Meta:
        verbose_name = _('компания')
        verbose_name_plural = _('компании')

    def __str__(self):
        return self.name
    
    
class DeviceModel(ArchiveMixin, AsyncBaseModel):
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
    
    
class DeviceSeries(ArchiveMixin, AsyncBaseModel):
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
    
    
class Device(ArchiveMixin, AsyncBaseModel, QuantityMixin):
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

    def __str__(self):
        return self.name


class Supplier(ArchiveMixin, AsyncBaseModel):
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


