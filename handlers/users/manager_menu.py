from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.markdown import hcode

from data.config import ADMINS
from keyboards.inline.menu import back_to_manager_menu, manager_keyboard
from loader import dp, db


    ###############
    # All employees
    ###############


from states.manager_states import Manager_States
from utils.misc.show_on_map import show


@dp.callback_query_handler(text="all_employees_info")
async def get_employees_info(call: CallbackQuery):
    employees = await db.select_all_users()
    count = 0
    for i in employees:
        count += 1

    if count <= 0:
        await call.message.edit_text("База данных пуста")
        await call.message.edit_reply_markup(back_to_manager_menu)
    else:
        for employee in employees:
            emp = await call.message.answer(f"Имя: {employee[1]}\n"
                                      f"Штрафы: {employee[2]}")
            employee_list.append(emp)
        await call.message.edit_reply_markup(back_to_manager_menu)

    ###########
    # Database
    ###########
database_list = []
@dp.callback_query_handler(text="database")
async def get_info(call: CallbackQuery):
    info = await db.select_data(id=int(ADMINS[0]))
    url = show(lat=info[1], lon=info[2])
    await call.message.edit_text(hcode("Начало работы: {start_time}\n"
                                    "Допустимая минута: {allowed_time} мин\n"
                                    "Штраф: {fine} сом\n"
                                    "Увеличенный штрф: {increased_fine} сом\n"
                                    "Кол-во дней: {charge}\n"
                                    "Пароль = {password}".format(**info)))
    location = await call.message.answer_location(info[1], info[2])
    google_location = await call.message.answer("Мы на Google карте\n"
                              f"<a href='{url}'>Google</a>", disable_web_page_preview=True)
    await call.message.edit_reply_markup(back_to_manager_menu)
    database_list.append(location)
    database_list.append(google_location)

    ###############
    # Set Main GPS
    ###############

@dp.callback_query_handler(text="set_main_GPS")
async def get_gps(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Здесь вы установите местоположение вашего учреждения на карте\n"
                                 "Нажмите на кнопку, чтобы отправить нам данные о местоположении\n"
                                 "Примечание!!!\n"
                                 "Будут использованы данные вашего текущего местоположения\n"
                                 "Вы должны быть внутри здания где находится учреждение\n"
                                 "И отправить эти данные можно только со смартфона(ПК не подходит)")

    await call.message.edit_reply_markup(back_to_manager_menu)
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.get_main_GPS.set()


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=Manager_States.get_main_GPS)
async def update_info_gps(message: types.Message, state: FSMContext):
    location = message.location
    lat = location.latitude
    lon = location.longitude
    msg = await message.answer(text="text", reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    await db.update_data_gps(lat, lon, int(ADMINS[0]))
    info = await db.select_data(id=int(ADMINS[0]))
    await message.answer(hcode("latitude={latitude}\n"
                               "longitude={longitude}".format(**info)))
    await state.finish()

    ##########
    # Password
    ##########

@dp.callback_query_handler(text="change_password")
async def change_password(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите новый пароль")
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.change_password.set()

@dp.message_handler(state=Manager_States.change_password)
async def update_password(message: types.Message, state: FSMContext):
    await db.update_data_password(message.text, int(ADMINS[0]))
    await state.finish()
    await message.answer("Пароль успешно изменен")


    #############
    # Start Time
    #############

@dp.callback_query_handler(text="start_time")
async def change_start_time(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите время начло работы \n"
                              "Например: Если работа начинается в 8, введите 8 \n"
                              "Если в 15, введите 15")
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.new_start_time.set()

@dp.message_handler(state=Manager_States.new_start_time)
async def update_start_time(message: types.Message, state: FSMContext):
    await db.update_data_start_time(int(message.text), int(ADMINS[0]))
    await state.finish()
    await message.answer("Время начало работы установлено")


    ###############
    # Allowed Time
    ###############

@dp.callback_query_handler(text="allowed_time")
async def change_start_time(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите на сколько минут можно опоздать после начало работы")
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.new_allowed_time.set()

@dp.message_handler(state=Manager_States.new_allowed_time.set())
async def update_allowed_time(message: types.Message, state: FSMContext):
    await db.update_data_allowed_time(int(message.text), int(ADMINS[0]))
    await state.finish()
    await message.answer("Допустимая минута для опоздания установлено")


    ###############
    # Fine
    ###############

@dp.callback_query_handler(text="fine")
async def change_start_time(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите штраф для опоздавших")
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.new_fine.set()

@dp.message_handler(state=Manager_States.new_fine)
async def update_fine(message: types.Message, state: FSMContext):
    await db.update_data_fine(int(message.text), int(ADMINS[0]))
    await state.finish()
    await message.answer("Штраф установлен")


    ###############
    # Increased Fine
    ###############

@dp.callback_query_handler(text="increased_fine")
async def change_start_time(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите увеличенный штраф для опоздавших несколько дней подряд")
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.new_increased_fine.set()

@dp.message_handler(state=Manager_States.new_increased_fine)
async def update_fine(message: types.Message, state: FSMContext):
    await db.update_data_increased_fine(int(message.text), int(ADMINS[0]))
    await state.finish()
    await message.answer("Увеличенный штраф установлен")


    ###############
    # Charge
    ###############

@dp.callback_query_handler(text="charge")
async def change_start_time(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Это кол-во подряд опоздавших дней, после которых сотрудникам будет начисляться увеличенный штраф\n"
                                 "Введите через сколько будет начисляться такой штраф")
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.new_charge.set()

@dp.message_handler(state=Manager_States.new_charge)
async def update_fine(message: types.Message, state: FSMContext):
    await db.update_data_charge(int(message.text), int(ADMINS[0]))
    await state.finish()
    await message.answer("Установлено")

@dp.callback_query_handler(text="restore")
async def restore_users_info(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите пароль")
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.password_to_restore.set()

@dp.message_handler(state=Manager_States.password_to_restore)
async def restoring_users_data(message: types.Message, state: FSMContext):
    info = await db.select_data(id=int(ADMINS[0]))
    if message.text == info[8]:
        await db.restore_employee_data(0, 0)
        await state.finish()
        await message.answer("Данные о штрафах сотрудников обновлены", reply_markup=manager_keyboard)
    else:
        await state.finish()
        await message.answer("Неверный пароль", reply_markup=manager_keyboard)
        await state.finish()


@dp.callback_query_handler(text="add_new_employee")
async def add_new_employee(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Переотправьте сообщение пользователя, которого вы хотите добавить в базу данных как сотрудник")
    await call.message.edit_reply_markup(back_to_manager_menu)
    await Manager_States.add_a_new_employee.set()

@dp.message_handler(state=Manager_States.add_a_new_employee)
async def adding_a_new_employee(message: types.Message, state: FSMContext):
    id = message.forward_from.id
    name = message.forward_from.full_name
    new_employee = await db.select_user(id=id)

    if new_employee != None:
        await message.answer("Этот сотрудник уже есть в базе данных")
        await state.finish()
    else:
        await db.add_user(id=id, name=name)
        await message.answer("Сотрудник добавлен в базу данных",
                             reply_markup=manager_keyboard)
        await state.finish()

employee_list = []
@dp.callback_query_handler(text="delete_employee")
async def delete_employee(call: CallbackQuery, state: FSMContext):
    all_employees = await db.select_all_users()
    await call.message.edit_text("Введите id сотрудника, чтобы удалить",
                                 reply_markup=back_to_manager_menu)
    for employee in all_employees:
        msg = await call.message.answer(f"Имя: {employee[1]}\n"
                                  f"id: {employee[0]}")
        employee_list.append(msg)
    await Manager_States.delete_employee.set()

@dp.message_handler(state=Manager_States.delete_employee)
async def deleting_employee(message: types.Message, state: FSMContext):
    id = int(message.text)
    employee = await db.select_user(id=id)
    if employee == None:
        await message.answer("Такого сотрудника нет в базе")
        await state.finish()
    else:
        for msg in employee_list:
            await msg.delete()
        employee_list.clear()
        await db.delete_user(id=id)
        await message.answer("Данные этого сотрудника удалены из базы данных",
                             reply_markup=manager_keyboard)
        await state.finish()