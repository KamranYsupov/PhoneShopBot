from django.contrib import admin

from .models import Settings
from ...admin.mixins import SingletonModelAdmin


@admin.register(Settings)
class SettingsAdmin(SingletonModelAdmin):
    pass