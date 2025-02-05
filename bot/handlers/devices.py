import os

import loguru
from aiogram import Router, types, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from bot.keyboards.inline import (
    get_inline_keyboard,
    inline_cancel_keyboard,
)
from bot.utils.message import get_device_info_message
from bot.utils.validators import validate_quantity
from bot.utils.pagination import (
    Paginator, 
    get_pagination_buttons,
    get_pagination_sizes
)
from bot.models import (
    TelegramUser, 
    CartItem,
    DeviceCompany,
    DeviceModel,
    DeviceSeries, 
    Device
)
from bot.handlers.state import CartItemState
from bot.orm.cart import add_to_cart, get_cart_quantity
from web.apps.devices.service import export_devices_to_excel

router = Router()


@router.callback_query(F.data.startswith('companies_'))
async def device_companies_callback_query(
    callback: types.CallbackQuery
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 10
    message_text = 'Выберите производителя устройств'
    
    device_companies = await DeviceCompany.objects.a_all()
    paginator = Paginator(
        array=device_companies,
        per_page=per_page,
        page_number=page_number
    )
    buttons = {
        company.name: f'com_{company.id}_{page_number}_1'
        for company in paginator.get_page()
    }
    pagination_buttons = get_pagination_buttons(
        paginator, prefix='companies'
    )
    sizes = (1,) * per_page
    if not pagination_buttons:
        pass
    elif len(pagination_buttons.items()) == 1:
        sizes += (1, 1)
    else:
        sizes += (2, 1)
    
    buttons.update(pagination_buttons)
    buttons['Назад 🔙'] = 'menu'
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes,
        ),
        parse_mode='HTML',
    )

    
@router.callback_query(F.data.startswith('com_'))
async def device_company_callback_query(
    callback: types.CallbackQuery
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 10
    previous_page_number = int(callback.data.split('_')[-2])
    company_id = callback.data.split('_')[-3]

    company = await DeviceCompany.objects.aget(id=company_id)
    message_text = f'Список моделей <b>{company.name}</b>:'
    device_models = await sync_to_async(list)(company.models.all())

    paginator = Paginator(
        array=device_models,
        per_page=per_page,
        page_number=page_number
    )
    buttons = {
        model.name: f'mod_{model.id}_{page_number}_1'
        for model in paginator.get_page()
    }    
    pagination_buttons = get_pagination_buttons(
        paginator, prefix=f'com_{company_id}_{previous_page_number}'
    )
    sizes = (1,) * per_page + get_pagination_sizes(
        pagination_buttons
    )
        
    buttons.update(pagination_buttons)
    buttons['Назад 🔙'] = f'companies_{previous_page_number}'
        
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes,
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data.startswith('mod_'))
async def device_model_callback_query(
    callback: types.CallbackQuery
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 10
    previous_page_number = int(callback.data.split('_')[-2])
    model_id = callback.data.split('_')[-3]

    model = await DeviceModel.objects.aget(id=model_id)
    message_text = f'Выберите серию <b>{model.name}</b>'
    device_series = await sync_to_async(list)(model.series.all()) 
    paginator = Paginator(
        array=device_series,
        per_page=per_page,
        page_number=page_number
    )
    
    buttons = {
        series.name: f'ser_{series.id}_{page_number}_1'
        for series in paginator.get_page()
    }
    pagination_buttons = get_pagination_buttons(
        paginator, prefix=f'mod_{model_id}_{previous_page_number}'
    )
    sizes = (1,) * per_page + get_pagination_sizes(
        pagination_buttons
    )
    
    buttons.update(pagination_buttons)
    buttons['Назад 🔙'] = \
        f'com_{model.company_id}_1_{previous_page_number}'
        
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes,
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data.startswith('ser_'))
async def device_series_callback_query(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    await state.clear()
    
    page_number = int(callback.data.split('_')[-1])
    per_page = 10
    previous_page_number = int(callback.data.split('_')[-2])
    series_id = callback.data.split('_')[-3]

    series = await DeviceSeries.objects.aget(id=series_id)
    message_text = f'Список устройств <b>{series.name}</b>:'
    devices = await sync_to_async(list)(series.devices.all()) 
    paginator = Paginator(
        array=devices,
        per_page=per_page,
        page_number=page_number
    )
    buttons = {
        device.name: f'dev_{device.id}_{page_number}_1'
        for device in paginator.get_page()
    }
    pagination_buttons = get_pagination_buttons(
        paginator, prefix=f'ser_{series_id}_{previous_page_number}'
    )
    sizes = (1,) * per_page + get_pagination_sizes(
        pagination_buttons
    )
    
    buttons.update(pagination_buttons)
    buttons['Назад 🔙'] = \
        f'mod_{series.model_id}_1_{previous_page_number}'
        
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes,
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data.startswith('dev_'))
async def device_callback_query(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 10
    previous_page_number = int(callback.data.split('_')[-2])
    device_id = callback.data.split('_')[-3]
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=callback.from_user.id
    )
    device = await Device.objects.aget(id=device_id)
    cart_quantity = await get_cart_quantity(
        device_id=device.id,
        telegram_user_id=telegram_user.id,
    )
    
    message_text = get_device_info_message(device, cart_quantity)
    message_text += '\nУкажите количество.'
    
    await state.update_data(
        device_id=device_id,
        previous_page_number=previous_page_number
    )
    await state.set_state(CartItemState.quantity)
    
    buttons = {}
    if cart_quantity:
        buttons.update({
            'Убрать из корзины 🗑': f'rm_from_cart_{device_id}',
            'Корзина 🛒': 'cart_1',
        })
    
    buttons.update({
        'Назад 🔙': \
            f'ser_{device.series_id}_1_{previous_page_number}',
        'Вернутся в меню 📁': 'menu',
    })
    
    reply_markup = get_inline_keyboard(
        buttons=buttons,
        sizes=(1, ) * 4
    )
        
    await callback.message.edit_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='HTML',
    )
    
    
@router.message(F.text, CartItemState.quantity)
async def add_to_cart_message_handler(
    message: types.Message,
    state: FSMContext,
):
    state_data = await state.get_data()
    previous_page_number = state_data.get('previous_page_number', 1)
    device = await Device.objects.aget(id=state_data['device_id'])
    
    quantity = await validate_quantity(
        message, 
        device.quantity,
        message.text,
    )
    if not quantity:
        return
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )  
    cart_item = await add_to_cart(
        device_id=device.id,
        telegram_user_id=telegram_user.id,
        quantity=quantity
    )
    if not cart_item:
        return 
    
    await state.clear()
    await state.update_data(device_id=device.id)
    await state.set_state(CartItemState.quantity)
    
    message_text = get_device_info_message(
        device,
        cart_item.quantity
    )
    message_text += '\nУкажите количество.'
    
    buttons = {
        'Убрать из корзины 🗑': f'rm_from_cart_{device.id}',
        'Корзина 🛒': 'cart_1',
        'Назад 🔙': \
            f'ser_{device.series_id}_1_{previous_page_number}',
        'Вернутся в меню 📁': 'menu',
    }
    

    await message.answer(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, ) * 4
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data == 'excel_devices')
async def export_devices_to_excel_callback_handler(
    callback: types.CallbackQuery,
    bot: Bot,
):
    await callback.message.edit_text(
        '<em>Подождите немного ...</em>',
        parse_mode='HTML',
    )
    
    file_name = 'devices.xlsx'
    await sync_to_async(export_devices_to_excel)(file_name)
    file_input = types.FSInputFile(file_name)
    
    await callback.message.delete()
    await bot.send_document(
        callback.message.chat.id, file_input
    )
    
    os.remove(file_name)