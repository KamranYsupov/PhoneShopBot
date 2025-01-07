from aiogram import Router

from .start import router as start_router
from .devices import router as devices_router
from .menu import router as menu_router
from .cart import router as cart_router
from .orders import router as orders_router

def get_main_router():
    main_router = Router()

    main_router.include_router(start_router)
    main_router.include_router(devices_router)
    main_router.include_router(menu_router)
    main_router.include_router(cart_router)
    main_router.include_router(orders_router)

    return main_router