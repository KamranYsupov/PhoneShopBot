from django.urls import path
from .views import download_devices_excel  # Импортируйте ваш view

urlpatterns = [
    path('export-devices/', download_devices_excel, name='export_devices'),
]