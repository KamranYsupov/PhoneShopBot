from django.urls import path
from .views import upload_devices_excel

urlpatterns = [
    path('upload-devices-excel/', upload_devices_excel, name='upload_devices_excel'),
]