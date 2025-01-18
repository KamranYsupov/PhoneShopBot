from aiogram import types
from aiogram.exceptions import TelegramBadRequest


async def edit_text_or_answer(
    message: types.Message,
    *args, **kwargs,
):
    try:
        await message.edit_text(*args, **kwargs)
    except TelegramBadRequest:
        await message.answer(*args, **kwargs)
    