import loguru
from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from keyboards.inline import (
    get_inline_keyboard,
    inline_cancel_keyboard,
    get_device_inline_keyboard
)
from utils.message import get_device_info_message
from utils.validators import validate_quantity
from models import (
    TelegramUser, 
    CartItem,
    DeviceCompany,
    DeviceModel,
    DeviceSeries, 
    Device
)
from .state import CartItemState
from orm.cart import add_to_cart, get_cart_quantity

router = Router()


@router.callback_query(F.data.startswith('companies_'))
async def device_companies_callback_query(
    callback: types.CallbackQuery
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 5
    message_text = 'Выберите производителя устройств'
    
    device_companies = await DeviceCompany.objects.a_all()
    
    buttons = {
        company.name: f'com_{company.id}_{page_number}_1'
        for company in device_companies
    }
    buttons['Назад 🔙'] = 'menu'
    
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, ) * per_page,
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data.startswith('com_'))
async def device_company_callback_query(
    callback: types.CallbackQuery
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 5
    previous_page_number = int(callback.data.split('_')[-2])
    company_id = callback.data.split('_')[-3]

    company = await DeviceCompany.objects.aget(id=company_id)
    message_text = f'Список моделей <b>{company.name}</b>:'
    device_models = await sync_to_async(list)(company.models.all())
    
    buttons = {
        model.name: f'mod_{model.id}_{page_number}_1'
        for model in device_models
    }
    buttons['Назад 🔙'] = f'companies_{previous_page_number}'
        
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, ) * per_page,
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data.startswith('mod_'))
async def device_model_callback_query(
    callback: types.CallbackQuery
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 5
    previous_page_number = int(callback.data.split('_')[-2])
    model_id = callback.data.split('_')[-3]

    model = await DeviceModel.objects.aget(id=model_id)
    message_text = f'Выберите серию <b>{model.name}</b>'
    device_series = await sync_to_async(list)(model.series.all()) 
    
    buttons = {
        series.name: f'ser_{series.id}_{page_number}_1'
        for series in device_series
    }
    buttons['Назад 🔙'] = \
        f'com_{model.company_id}_{previous_page_number}_{page_number}'
        
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, ) * per_page,
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
    per_page = 5
    previous_page_number = int(callback.data.split('_')[-2])
    series_id = callback.data.split('_')[-3]

    series = await DeviceSeries.objects.aget(id=series_id)
    message_text = f'Список устройств <b>{series.name}</b>:'
    devices = await sync_to_async(list)(series.devices.all()) 
    
    buttons = {
        device.name: f'dev_{device.id}_{page_number}_1'
        for device in devices
    }
    
    buttons['Назад 🔙'] = \
        f'mod_{series.model_id}_{previous_page_number}_{page_number}'
        
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, ) * per_page,
        ),
        parse_mode='HTML',
    )
    
    
@router.callback_query(F.data.startswith('dev_'))
async def device_callback_query(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    page_number = int(callback.data.split('_')[-1])
    per_page = 5
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
    
    await state.update_data(device_id=device_id)
    await state.set_state(CartItemState.quantity)
    
    if cart_quantity:
        reply_markup = get_device_inline_keyboard(device.id)
    else:
        buttons = {
            'Вернутся в меню 📁': 'menu',
            'Назад 🔙': \
                f'ser_{device.series_id}_{previous_page_number}_{page_number}'
        }
        reply_markup = get_inline_keyboard(
            buttons=buttons,
            sizes=(1, 1, 1)
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

    await message.answer(
        message_text,
        reply_markup=get_device_inline_keyboard(device.id),
        parse_mode='HTML',
    )