from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib import messages

from web.apps.bot_settings.models import BotSettings    


@staff_member_required
def change_bot_status_view(request):

    if request.method != 'GET':
        return HttpResponse('Метод не поддерживается.', status=405)
    
    bot_settings = BotSettings.get_instance()
    
    if bot_settings.is_active:
        bot_settings.is_active = False 
        messages.warning(request, 'Бот выключен')
        
    else:
        bot_settings.is_active = True
        messages.info(request, 'Бот запущен')

    bot_settings.save() 
    
    return redirect('admin:telegram_users_telegramuser_changelist')
    
    