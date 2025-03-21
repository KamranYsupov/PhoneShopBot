import pandas as pd
from io import BytesIO
from django.db import transaction
from django.db.models import Case, When, Value, IntegerField
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
    whens = [
        When(series__model__company__name=company, then=Value(idx))
        for idx, company in enumerate(settings.DEVICE_COMPANY_ORDER)
    ]

    return Device.objects.select_related(
        'series__model__company'
    ).annotate(
        sort_order=Case(
            *whens,
            default=Value(len(settings.DEVICE_COMPANY_ORDER)),  # Все остальные компании в конце
            output_field=IntegerField()
        )
    ).order_by('sort_order')


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
        for model in (DeviceCompany, Supplier):
            model.objects.all().delete()

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
