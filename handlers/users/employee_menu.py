from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.markdown import hcode

from data.config import ADMINS
from keyboards.inline.menu import location_button, back_to_employee_menu
from loader import dp, db


###############
# Add employee
###############
from utils.misc.calc_distance import calc_distance


# @dp.callback_query_handler(text="add_me")
# async def add_new_employee(call: CallbackQuery):
#     user = await db.select_user(id=int(call.from_user.id))
#     if user == None:
#         await db.add_user(call.from_user.id, call.from_user.full_name)
#         await call.message.edit_text("Вы добавлены в базу данных")
#         await call.message.edit_reply_markup(back_to_employee_menu)
#     else:
#         await call.message.edit_text("Вы уже добавлены в базу данных")
#         await call.message.edit_reply_markup(back_to_employee_menu)


    ##################################
    # Show employee's info to employee
    ##################################

@dp.callback_query_handler(text="employee_info")
async def show_info(call: CallbackQuery):
    user = await db.select_user(id=int(call.from_user.id))

    if user == None:
        await call.message.edit_text("Вас нет в базе данных\n"
                                  "Сначла мы должны добавить вас в базу данных\n"
                                  "Для этого нажмите на кнопку Добавить меня")
        await call.message.edit_reply_markup(back_to_employee_menu)
    else:
        await call.message.edit_text(hcode("Имя: {name}\n"
                                        "Штрафы: {fine}\n"
                                        "Кол-во опоздавших дней: {charge}\n"
                                        "Отмечался: {was_noted}\n"
                                        "День: {day}".format(**user)))
        await call.message.edit_reply_markup(back_to_employee_menu)


    ###############################
    # Get employee's GPS and check
    ###############################

@dp.callback_query_handler(text="employee_arrived")
async def check_employee(call: CallbackQuery, state: FSMContext):
    employee = await db.select_user(id=call.from_user.id)
    if employee == None:
        await call.message.edit_text("Вас нет в базе данных\n"
                                  "Сначла мы должны добавить вас в базу данных\n"
                                  "Для этого нажмите на кнопку Добавить меня")
        await call.message.edit_reply_markup(back_to_employee_menu)
    else:
        if employee[5] == call.message.date.day:
            await call.message.edit_text("Вы сегодня уже отмечались")
            await call.message.edit_reply_markup(back_to_employee_menu)
        else:
            await call.message.answer("Нажмите на кнопку, чтобы отправить свое местоположение",
                                      reply_markup=location_button)

            await state.set_state("get_employee_GPS")

@dp.message_handler(content_types=types.ContentTypes.LOCATION, state="get_employee_GPS")
async def check_employee_GPS(message: types.Message, state: FSMContext):

    employee = await db.select_user(id=message.from_user.id)
    print(employee[5])
    location = message.location
    msg = await message.answer(text="text", reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    await state.finish()
    info = await db.select_data(id=int(ADMINS[0]))
    a = calc_distance(info[1], info[2], location.latitude, location.longitude)

    if a <= 50:
        info = await db.select_data(id=int(ADMINS[0]))
        time = info[3] * 60 + info[4]
        arrived_hour = message.date.hour
        arrived_minute = message.date.minute
        arrived_time = arrived_hour * 60 + arrived_minute
        await message.answer("Вы пришли на работу")
        charge = employee[3]
        fine = employee[2]

        if arrived_time > time:

            await message.answer(f"Вы опоздали на {arrived_time - time} мин")
            if charge + 1 < 3:
                fine += 200
                charge += 1
                await db.update_user_fine(fine, charge, message.from_user.id)
                await message.answer("Вам начислен штраф в размере 200 сом(сомов) \n"
                                     f"Ваш текущий штраф состовляет {fine} сом(сомов)",
                                     reply_markup=back_to_employee_menu)

            elif charge + 1 >= 3:
                fine += 500
                charge += 1
                await db.update_user_fine(fine, charge, message.from_user.id)
                await message.answer("Так как вы опоздывали 3 или более дней подряд \n"
                                     "вам начислен штраф в размере 500 сом(сомов) \n"
                                     f"Ваш текущий штраф состовляет {fine} сом(сомов)",
                                        reply_markup=back_to_employee_menu)

        else:
            await db.update_user_fine(fine, 0, message.from_user.id)
            await message.answer("Вы пришли во время\n"
                                 "Вы опоздали 0 дней/дня подряд\n"
                                 f"Ваш текущий штраф состовляет {fine} сом(сомов)",
                                 reply_markup=back_to_employee_menu)

        day = message.date.day
        await db.update_user_day(day, message.from_user.id)
    else:
        await message.answer(f"Вам надо пройти(проехать) {a} м \n"
                             "Вот сюда ⬇",
                             reply_markup=back_to_employee_menu)
        await message.answer_location(latitude=info[1], longitude=info[2])