from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

from .service import import_devices_from_excel, export_devices_to_excel

@staff_member_required
def upload_devices_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        try:
            import_devices_from_excel(excel_file)

            messages.success(request, 'Данные успешно загружены в базу данных.')
        except Exception as e:
            messages.error(request, f'Ошибка при обработке файла: {str(e)}')

        return redirect('admin:devices_device_changelist') 

    return HttpResponse("Метод не поддерживается.", status=405)


def download_devices_excel(request):
    """
    View для загрузки Excel-файла с данными устройств.
    """
    # Генерация Excel данных
    excel_data = export_devices_to_excel()

    # Подготовка ответа
    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="devices.xlsx"'

    return response