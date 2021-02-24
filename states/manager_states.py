from aiogram.dispatcher.filters.state import StatesGroup, State


class Manager_States(StatesGroup):
    get_main_GPS = State()
    change_password = State()
    new_start_time = State()
    new_allowed_time = State()
    new_fine = State()
    new_increased_fine = State()
    new_charge = State()
    password_to_restore = State()
    add_a_new_employee = State()
    delete_employee = State()