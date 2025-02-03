from django.urls import path
from .views import upload_devices_excel, download_devices_excel

urlpatterns = [
    path('upload-devices-excel/', upload_devices_excel, name='upload_devices_excel'),
    path('download-devices/', download_devices_excel, name='download_devices_excel'),
]