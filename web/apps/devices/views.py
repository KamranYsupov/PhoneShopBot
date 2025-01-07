from django.http import HttpResponse

from .service import export_devices_to_excel


def download_devices_excel(request):
    excel_file = export_devices_to_excel()

    response = HttpResponse(
        excel_file,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="devices.xlsx"'

    return response