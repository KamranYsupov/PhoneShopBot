from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib import messages

from .service import change_bot_status


@staff_member_required
def change_bot_status_view(request):

    if request.method == 'GET':
        change_bot_status()
        return redirect('admin:telegram_users_telegramuser_changelist')
    
    return HttpResponse("Метод не поддерживается.", status=405)