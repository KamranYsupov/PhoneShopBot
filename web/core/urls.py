from django.contrib import admin
from django.urls import path, include
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('devices/', include('web.apps.devices.urls')),
    path('bot/', include('web.apps.bot_settings.urls')),
    path('orders/', include('web.apps.orders.urls'))

]
