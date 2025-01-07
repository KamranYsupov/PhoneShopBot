from aiogram import Router

from .start import router as start_router
from .devices_menu import router as devices_menu_router

def get_main_router():
    main_router = Router()

    main_router.include_router(start_router)
    main_router.include_router(devices_menu_router)

    return main_router