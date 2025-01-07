from django.contrib import admin

from .models import (
    DeviceCompany, 
    DeviceModel, 
    DeviceSeries, 
    Device
)

class DeviceModelInline(admin.TabularInline):
    model = DeviceModel
    extra = 1
   

class DeviceSeriesInline(admin.TabularInline):
    model = DeviceSeries
    extra = 1
    
    
class DeviceInline(admin.TabularInline):
    model = Device
    fields = (
        'name',
        'quantity', 
        'price_from_1',
        'price_from_20'
    )
    extra = 1

     
@admin.register(DeviceCompany)
class DeviceCompanyAdmin(admin.ModelAdmin):
    inlines = (DeviceModelInline, )


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    inlines = (DeviceSeriesInline, )


@admin.register(DeviceSeries)
class DeviceSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'model')
    inlines = (DeviceInline, )

import pandas as pd

def export_devices_to_excel(file_name='devices.xlsx'):
    # Список для хранения данных
    data = []

    # Извлечение всех устройств и их связанных данных
    devices = Device.objects.select_related('series__model__company').all()
    
    for device in devices:
        data.append({
            'Название компании': device.series.model.company.name,
            'Название модели': device.series.model.name,
            'Название серии': device.series.name,
            'Название устройства': device.name,
            'Цена от 1': device.price_from_1,
            'Цена от 20': device.price_from_20,
            'Кол-во': device.quantity  # Предполагается, что поле quantity существует в QuantityMixin
        })

    # Создание DataFrame из списка данных
    df = pd.DataFrame(data)

    # Запись DataFrame в Excel файл
    df.to_excel(file_name, index=False)
    
    

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'series', 'quantity', 'price_from_1', 'price_from_20')
    list_editable = ('quantity', 'price_from_1', 'price_from_20')
    
    actions = [export_devices_to_excel]
