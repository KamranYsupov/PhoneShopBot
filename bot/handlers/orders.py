from datetime import datetime, date

import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from asgiref.sync import sync_to_async
from django.utils import timezone
from django.db.models import Q

from bot.keyboards.inline import (
    get_inline_keyboard,
)
from bot.keyboards.reply import (
    get_reply_keyboard,
    reply_keyboard_remove,
    reply_cancel_keyboard,
    get_reply_calendar_keyboard
)
from bot.handlers.state import OrderState, DateState
from bot.orm.orders import create_order
from bot.models import (
    TelegramUser,
    Device,
    DeviceCompany,
    DeviceModel,
    DeviceSeries, 
    CartItem, 
    Order, 
    OrderItem
)
from bot.utils.bot import edit_text_or_answer
from bot.utils.message import (
    get_order_message_and_buttons, 
    get_item_info_message,
    get_order_items_info_message
)
from bot.utils.pagination import Paginator, get_pagination_buttons
from bot.utils.calendar import get_all_months
from bot.utils.validators import get_integer_from_string

router = Router()


@router.callback_query(F.data == 'create_order')
async def create_order_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await state.set_state(OrderState.comment)
    
    await callback.message.delete()
    await callback.message.answer(
        'Укажите комментарий',
        reply_markup=get_inline_keyboard(
            buttons={'Пропустить ➡️': 'complete_create_order'}
        )
    )
    
    
@router.callback_query(F.data == 'complete_create_order')
async def complete_create_order_callback_handler(
    callback: types.CallbackQuery,
):
    await complete_create_order_handler(
        message=callback.message,
        telegram_id=callback.from_user.id,
    )
    

@router.message(F.text, OrderState.comment)
async def complete_create_order_message_handler(
    message: types.Message,
):
    await complete_create_order_handler(
        message=message,
        telegram_id=message.from_user.id,
        comment=message.text
    )
    
    
async def complete_create_order_handler(
    message: types.Message,
    telegram_id: int,
    comment: str | None = None,
):
    create_order_data = {'telegram_id': telegram_id}
    
    if comment:
        create_order_data['comment'] = comment
    else:
        comment = 'Без комментария'
        
    result = await create_order(**create_order_data)
    buttons = {
        'Корзина 🛒': 'cart_1',
        'Вернуться в меню 📁': 'menu'
    }
    
    if isinstance(result, Order):
        order = result
        order_items = await OrderItem.objects.afilter(
            order_id=order.id,
            select_relations=('device', )
        )        
        order_info_message, buttons = get_order_message_and_buttons(
            order_items
        )
        message_text = (
            f'Заказ <b>#{order.number}</b> успешно создан!\n\n'
            + order_info_message
            + f'\nКомментарий: <b>{comment}</b>'
        )
        
    elif isinstance(result, list):
        cart_items = result
        cart_items_names = [
            f'<b>{cart_item.device.name}</b>' for cart_item in cart_items
        ]
        message_text = (
            f'Количество устройств {", ".join(cart_items_names)} ' 
            'превышает количество на складе'
        )
    else:
        await callback.message.delete()
        return 
    
    await edit_text_or_answer(
        message,
        text=message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, 1)
        ),
        parse_mode='HTML'
    )
    await message.answer(
        '⏳Пожалуйста, подождите. Ваш заказ оформляется...'
    )
        

@router.callback_query(F.data.startswith('my_orders_'))
async def my_orders_callback_handler(
    callback: types.CallbackQuery,
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 5
    
    now = timezone.now()
    current_year = now.year
    
    years = sorted(
        list(range(2025, current_year + 1)),
        reverse=True
    )
    paginator = Paginator(
        array=years,
        page_number=page_number,
        per_page=per_page
    )
    buttons = {
        str(year): f'year_my_orders_{year}' 
        for year in paginator.get_page()
    }
    sizes = (1,) * per_page
    pagination_buttons = get_pagination_buttons(
        paginator, prefix='my_orders'
    )
    if len(pagination_buttons.items()) == 1:
        sizes += (1, 1)
    else:
        sizes += (2, 1)
        
    buttons.update(pagination_buttons)
    buttons['Вернуться в меню 📁'] = 'menu'
        
    await callback.message.edit_text(
        'Выберите год',
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes,
        )
    )
    
    
@router.callback_query(F.data.startswith('year_my_orders_'))
async def my_orders_year_callback_handler(
    callback: types.CallbackQuery,
):
    year = int(callback.data.split('_')[-1])
    now = timezone.now()
    
    months_names = get_all_months()
    
    if year == now.year:
        months_names = months_names[:now.month]
    
    buttons = {
        month_name: f'calendar_my_orders_{month_index + 1}_{year}'
        for month_index, month_name in enumerate(months_names)
    }  
    buttons['Вернуться в меню 📁'] = 'menu'
    
    sizes = (1,) * (len(buttons))  
    
    await callback.message.edit_text(
        'Выберите месяц',
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes,
        )
    )
    
    
@router.callback_query(F.data.startswith('calendar_my_orders_'))
async def my_orders_calendar_callback_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    month, year = map(int, callback.data.split('_')[-2:])
    
    await state.set_state(DateState.day)
    await state.update_data(year=year, month=month)
    
    await callback.message.delete()
    await callback.message.answer(
        'Выберите дату',
        reply_markup=get_reply_calendar_keyboard(
            year=year,
            month=month,
        )
    )
    
                    
@router.message(F.text, DateState.day)
async def my_orders_day_callback_handler(
    message: types.Message,
    state: FSMContext,
):
    day = get_integer_from_string(message.text)
    
    if not day:
        await message.answer('Пожалуйста, выберите день из календаря')
        return
        
    state_data = await state.get_data()
    order_date = date(
        state_data['year'],
        state_data['month'], 
        day
    )
    formated_order_date = order_date.strftime("%d.%m.%Y")
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    orders = await sync_to_async(list)(
        Order.objects.exclude(
            status__in=[Order.Status.ARRIVED, Order.Status.CANCELED]
        ).filter(
            buyer=telegram_user,
            created_at=order_date
        )
    )
    
    if not orders:
        await message.answer(
            f'{formated_order_date} нет заказов.'
        )
    else:
        message_text = await get_order_items_info_message(orders)
        message_text = (
            f'Заказы на день {formated_order_date}\n\n'
            + message_text
        )
        
        await message.answer(
            message_text,
            parse_mode='HTML',
        )
            
        
@router.callback_query(F.data.startswith('order_'))
async def order_callback_handler(
    callback: types.CallbackQuery,
):
    order_id = callback.data.split('_')[-1]
    
    order = await Order.objects.aget(id=order_id)
    order_items = await OrderItem.objects.afilter(
        order_id=order.id,
        select_relations=('device', )
    )
    order_message_text, _ = get_order_message_and_buttons(order_items)
    message_text = (
        f'<b>#{order.number}</b>\n\n'
        f'{order_message_text}\n'
    )
    
    await callback.message.edit_text(
        message_text,
        parse_mode='HTML'
    )
    
    