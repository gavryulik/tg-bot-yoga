from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    format = State()
    name = State()
    phone = State()
    day = State()
    time = State()
    receipt = State()