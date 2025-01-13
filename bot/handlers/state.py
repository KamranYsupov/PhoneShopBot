from aiogram.fsm.state import StatesGroup, State

    
class CartItemState(StatesGroup):
    device_id = State()
    quantity = State()


