from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .models import DeviceCompany, DeviceModel, DeviceSeries, Device

class DeviceModelInline(admin.TabularInline):
    model = DeviceModel
    extra = 1

class DeviceSeriesInline(admin.TabularInline):
    model = DeviceSeries
    extra = 1

class DeviceInline(admin.TabularInline):
    model = Device
    fields = ('name', 'quantity', 'price_from_1', 'price_from_20')
    extra = 1


@admin.register(DeviceCompany)
class DeviceCompanyAdmin(admin.ModelAdmin):
    inlines = (DeviceModelInline,)
    
    search_fields = [
        'name__iregex',
    ]


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    
    inlines = (DeviceSeriesInline,)
    list_filter = ('company',)  # Фильтрация по компании
    
    search_fields = [
        'name__iregex',
    ]


@admin.register(DeviceSeries)
class DeviceSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'model')
    inlines = (DeviceInline,)
    list_filter = ('model',)  # Фильтрация по модели
    
    search_fields = [
        'name__iregex',
    ]


class CompanyFilter(SimpleListFilter):
    title = _('Компания')
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        companies = DeviceCompany.objects.all()
        return [(company.id, company.name) for company in companies]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(series__model__company_id=self.value())
        return queryset


class ModelFilter(SimpleListFilter):
    title = _('Модель')
    parameter_name = 'model'

    def lookups(self, request, model_admin):
        models = DeviceModel.objects.all()
        return [(model.id, model.name) for model in models]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(series__model__id=self.value())
        return queryset
    
    
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'series', 'quantity', 'price_from_1', 'price_from_20')
    list_editable = ('quantity', 'price_from_1', 'price_from_20')
    list_filter = (CompanyFilter, ModelFilter, 'series') 
    
    search_fields = [
        'name__iregex',
    ]
