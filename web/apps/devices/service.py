import pandas as pd
from io import BytesIO
from django.db import transaction
from django.conf import settings
from openpyxl.utils import get_column_letter
import loguru

from .models import (
    Device,
    DeviceSeries,
    DeviceModel,
    DeviceCompany,
    Supplier,
)


def get_devices_sorted_by_company():
    company_priority = {
        company: idx for idx, company in
        enumerate(settings.DEVICE_COMPANY_ORDER)
    }

    series = sorted(
        list(DeviceSeries.objects
             .select_related('model__company')
             .prefetch_related('devices')
             ),
        key=lambda x: company_priority.get(
            x.model.company.name,
            len(settings.DEVICE_COMPANY_ORDER)
        )
    )

    devices = []
    for series_obj in series:
        devices.extend(series_obj.devices.all())

    return devices


def export_devices_to_excel(file_name: str):
    """
    Экспортирует данные устройств в Excel.
    """
    # Список для хранения данных
    data = []

    devices = get_devices_sorted_by_company()
    
    for device in devices:
        data.append({
            'Устройство': device.name,
            'Цена за 1 шт': device.price_from_1,
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

        # Получаем активный лист
        worksheet = writer.sheets['Sheet1']

        # Устанавливаем ширину столбцов
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).map(len).max(), len(col))  # Максимальная длина
            adjusted_width = (max_length + 2)  # Добавляем немного пространства
            worksheet.column_dimensions[get_column_letter(idx + 1)].width = adjusted_width

    with open(file_name, 'wb') as f:
        f.write(output.getvalue())


def import_devices_from_excel(excel_file):
    """Функция для импрота в данных из excel таблицы в бд"""
    df = pd.read_excel(excel_file)

    with transaction.atomic():
        object_ids = []

        for index, row in df.iterrows():
            company, _ = DeviceCompany.objects.get_or_create(name=row['company'])
            model, _ = DeviceModel.objects.get_or_create(name=row['model'], company=company)
            series, _ = DeviceSeries.objects.get_or_create(name=row['series'], model=model)
            supplier, _ = Supplier.objects.get_or_create(name=row['supplier'])
        
            try:
                quantity = int(row.get('quantity'))
            except ValueError:
                quantity = 100

            device, _ = Device.objects.update_or_create(
                name=row['device'],
                defaults={
                    'supplier': supplier,
                    'series': series,
                    'price_from_1': row['price_from_1'],
                    'price_from_20': row['price_from_20'],
                    'quantity': quantity
                }
            )
            object_ids.extend(
                (company.id, model.id, series.id, device.id, supplier.id)
            )

        for model in (DeviceCompany, DeviceModel, DeviceSeries, Device, Supplier):
            model.objects.exclude(id__in=object_ids).update(is_archived=True)



