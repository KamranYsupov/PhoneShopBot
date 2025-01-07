from aiogram import types

from typing import List, Optional, Union, Any

def get_integer_from_string(string: str) -> Optional[int]:
    try:
        integer = int(string)
        return integer
    except ValueError:
        return None
    

async def validate_quantity(
    message: types.Message,
    device_quantity: int,
    input_quantity: Any
) -> Union[int, None]:
    quantity = get_integer_from_string(input_quantity)
    
    if not quantity:
        await message.answer('Пожалуйста, отправьте корректное количество')
        return
    if quantity > device_quantity:
        await message.answer('Число не должно превышать количество на складе')
        return
    
    return quantity
    
     