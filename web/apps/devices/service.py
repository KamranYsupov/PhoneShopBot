import pandas as pd
from io import BytesIO
from .models import Device  # Импортируйте вашу модель Device


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
            'Компания': device.series.model.company.name,
            'Модель': device.series.model.name,
            'Серия': device.series.name,
            'Устройство': device.name,
            'Цена от 1': device.price_from_1,
            'Цена от 20': device.price_from_20,
            'Количество': device.quantity
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