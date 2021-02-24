from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data.config import ADMINS
from handlers.users.customer_menu import where_is_msgs
from handlers.users.manager_menu import database_list, employee_list
from keyboards.inline.menu import inline_choose_menu, customer_menu, employee_keyboard, manager_keyboard
from loader import dp, db
from states.manager_states import Manager_States


@dp.callback_query_handler(text="back_to_choose_menu")
async def back_to_choose_menu_def(call: CallbackQuery):
    await call.message.edit_text(f"Привет, {call.from_user.full_name}! \n"
                         "Подскажите нам, кто вы?")
    await call.message.edit_reply_markup(inline_choose_menu)

@dp.callback_query_handler(text="back_to_customer_menu", state="contact")
@dp.callback_query_handler(text="back_to_customer_menu")
@dp.callback_query_handler(text="customer")
async def customer_menu_def(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Добро пожаловать")
    await call.message.edit_reply_markup(customer_menu)
    for msg in where_is_msgs:
        await msg.delete()
    where_is_msgs.clear()


@dp.callback_query_handler(text="back_to_employee_menu", state="get_employee_GPS")
@dp.callback_query_handler(text="back_to_employee_menu")
@dp.callback_query_handler(text="employee")
async def employee_menu(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Добро пожаловать")
    await call.message.edit_reply_markup(employee_keyboard)
    await state.finish()


@dp.callback_query_handler(text="back_to_manager_menu", state = Manager_States.all_states)
@dp.callback_query_handler(text="back_to_manager_menu")
@dp.callback_query_handler(text="manager")
async def manager_menu(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if str(user_id) in ADMINS:
        await call.message.edit_text(f"Добро пожаловать, {call.from_user.full_name}\n"
                                     "Здесь вы можете редактировать данные")
        await call.message.edit_reply_markup(manager_keyboard)
        await state.finish()
        for msg in database_list:
            await msg.delete()
        database_list.clear()

        for emp in employee_list:
            await emp.delete()
        employee_list.clear()
    else:
        await call.message.answer("Посторонним вход запрещен")
