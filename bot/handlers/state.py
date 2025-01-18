from aiogram.fsm.state import StatesGroup, State

    
class CartItemState(StatesGroup):
    device_id = State()
    quantity = State()
    
    
class OrderState(StatesGroup):
    comment = State()


class DateState(StatesGroup):
    year = State()
    month = State() 
    day = State() 

