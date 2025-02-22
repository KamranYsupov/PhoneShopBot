import pandas as pd
from io import BytesIO
from django.db import transaction

from .models import (
    Device,
    DeviceSeries,
    DeviceModel,
    DeviceCompany,
    Supplier,
)


def export_devices_to_excel(file_name=None):
    """
    Экспортирует данные устройств в Excel.
    
    :param file_name: Если указан, сохраняет файл на сервере. Если None, возвращает бинарные данные.
    :return: Если file_name=None, возвращает бинарные данные (BytesIO). Иначе возвращает None.
    """
    # Список для хранения данных
    data = []

    devices = Device.objects.select_related(
        'series__model__company'
    ).all()
    
    for device in devices:
        data.append({
            'Устройство': device.name,
            'Цена за 1 шт': device.price_from_1,
        })

    df = pd.DataFrame(data)

    if file_name:
        df.to_excel(file_name, index=False)
        return None

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    excel_data = output.getvalue()
    return excel_data


def import_devices_from_excel(excel_file):
    """Функция для импрота в данных из excel таблицы в бд"""
    df = pd.read_excel(excel_file)

    with transaction.atomic():
        for index, row in df.iterrows():
            company, _ = DeviceCompany.objects.get_or_create(name=row['company'])
            model, _ = DeviceModel.objects.get_or_create(name=row['model'], company=company)
            series, _ = DeviceSeries.objects.get_or_create(name=row['series'], model=model)
            supplier, _ = Supplier.objects.get_or_create(name=row['supplier'])
        
            try:
                quantity = int(row.get('quantity'))
            except ValueError:
                quantity = 100

            Device.objects.update_or_create(
                name=row['device'],
                defaults={
                    'supplier': supplier,
                    'series': series,
                    'price_from_1': row['price_from_1'],
                    'price_from_20': row['price_from_20'],
                    'quantity': quantity
                }
            )