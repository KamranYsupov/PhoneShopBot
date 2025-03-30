from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .models import (
    DeviceCompany,
    DeviceModel,
    DeviceSeries, 
    Device,
    Supplier,
)
from ...admin.mixins import ArchiveModelAdminMixin


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
class DeviceCompanyAdmin(ArchiveModelAdminMixin):
    inlines = (DeviceModelInline,)
    
    search_fields = [
        'name__iregex',
    ]


@admin.register(DeviceModel)
class DeviceModelAdmin(ArchiveModelAdminMixin):
    list_display = ('name', 'company')
    
    inlines = (DeviceSeriesInline,)
    list_filter = ('company',)  # Фильтрация по компании
    
    search_fields = [
        'name__iregex',
    ]


@admin.register(DeviceSeries)
class DeviceSeriesAdmin(ArchiveModelAdminMixin):
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
        companies = DeviceCompany.objects.filter(is_archived=False)
        return [(company.id, company.name) for company in companies]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                series__model__company_id=self.value()
            )
        return queryset


class ModelFilter(SimpleListFilter):
    title = _('Модель')
    parameter_name = 'model'

    def lookups(self, request, model_admin):
        models = DeviceModel.objects.filter(is_archived=False)
        return [(model.id, model.name) for model in models]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                is_archived=False,
                series__model__id=self.value()
            )
        return queryset
    

class SeriesFilter(SimpleListFilter):
    title = _('Серия')
    parameter_name = 'series'

    def lookups(self, request, model_admin):
        series = DeviceSeries.objects.filter(is_archived=False)
        return [(series_obj.id, series_obj.name) for series_obj in series]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                is_archived=False,
                series__id=self.value()
            )
        return queryset


class SupplierFilter(SimpleListFilter):
    title = _('Поставщик')
    parameter_name = 'supplier'

    def lookups(self, request, model_admin):
        suppliers = Supplier.objects.filter(is_archived=False)
        return [(supplier.id, supplier.name) for supplier in suppliers]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                is_archived=False,
                supplier__id=self.value()
            )
        return queryset


@admin.register(Device)
class DeviceAdmin(ArchiveModelAdminMixin):
    list_display = ('name', 'series', 'supplier', 'quantity', 'price_from_1', 'price_from_20')
    list_editable = ('quantity', 'price_from_1', 'price_from_20')
    list_filter = (CompanyFilter, ModelFilter, SeriesFilter, SupplierFilter)
    
    search_fields = [
        'name__iregex',
        'supplier__name__iregex'
    ]

    
@admin.register(Supplier)
class SupplierAdmin(ArchiveModelAdminMixin):
    search_fields = [
        'name__iregex',
    ]
