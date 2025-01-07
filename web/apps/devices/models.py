from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import AsyncBaseModel


class DeviceCompany(AsyncBaseModel):
    """Модель компании устройства"""
    name = models.CharField(
        _("Название"),
        max_length=100,
        unique=True,
        db_index=True,
    )
    
    class Meta:
        verbose_name = _("Компания")
        verbose_name_plural = _("Компании")

    def __str__(self):
        return self.name
    
    
class DeviceModel(AsyncBaseModel):
    """Модель модели устройства"""
    name = models.CharField(
        _("Название"),
        max_length=100,
        unique=True,
        db_index=True,
    )
    
    company = models.ForeignKey(
        "devices.DeviceCompany",
        verbose_name=_("Компания"), 
        on_delete=models.CASCADE,
        related_name='models'
    )
    
    class Meta:
        verbose_name = _("Модель")
        verbose_name_plural = _("Модели")

    def __str__(self):
        return self.name
    
    
class DeviceSeries(AsyncBaseModel):
    """Модель серии модели устройства"""
    name = models.CharField(
        _("Название"),
        max_length=100,
        unique=True,
        db_index=True,
    )
    
    model = models.ForeignKey(
        "devices.DeviceModel",
        verbose_name=_("Модель"), 
        on_delete=models.CASCADE,
        related_name='series'
    )
    
    class Meta:
        verbose_name = _("Серия")
        verbose_name_plural = _("Серии")

    def __str__(self):
        return self.name
    
    
class Device(AsyncBaseModel):
    """Модель устройства"""
    name = models.CharField(
        _("Название"),
        max_length=200,
        unique=True,
        db_index=True,
    )
    price = models.FloatField(_("Цена"))
    
    series = models.ForeignKey(
        "devices.DeviceSeries",
        verbose_name=_("Серия"), 
        on_delete=models.CASCADE,
        related_name='devices'
    )
    
    class Meta:
        verbose_name = _("Устройство")
        verbose_name_plural = _("Устройства")

    def __str__(self):
        return self.name



