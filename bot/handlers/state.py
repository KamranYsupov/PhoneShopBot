from aiogram.fsm.state import StatesGroup, State

    
class CartItemState(StatesGroup):
    device_id = State()
    quantity = State()
    previous_page_number = State()
    
    
class OrderState(StatesGroup):
    comment = State()


class DateState(StatesGroup):
    year = State()
    month = State() 
    day = State() 

