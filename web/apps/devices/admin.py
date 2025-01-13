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
    inlines = (DeviceInline, )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass
