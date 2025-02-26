from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib import messages

from web.apps.orders.service import send_orders_info


@staff_member_required
def send_orders_info_view(request):
    if request.method != 'GET':
        return HttpResponse('Метод не поддерживается.', status=405)

    send_orders_info()
    messages.info(request, 'Аналитика успешно отправлена')

    return redirect('admin:orders_order_changelist')

