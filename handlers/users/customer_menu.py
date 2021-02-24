from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.types import CallbackQuery

from keyboards.inline.menu import back_to_customer_menu
from loader import dp, db

from data.config import ADMINS, GROUP
from utils.misc.show_on_map import show


@dp.callback_query_handler(text="services")
async def services_menu(call: CallbackQuery):
    await call.message.edit_text("Услуги")
    await call.message.edit_reply_markup(back_to_customer_menu)

where_is_msgs = []
@dp.callback_query_handler(text="where_is")
async def where_is_menu(call: CallbackQuery):
    info = await db.select_data(id=int(ADMINS[0]))
    url = show(lat=info[1], lon=info[2])
    await call.message.edit_text("🗺")
    we_text = await call.message.answer("Мы находимся здесь")
    location_text = await call.message.answer_location(latitude=info[1], longitude=info[2])
    google_location = await call.message.answer("Мы на Google карте\n"
        f"<a href='{url}'>Google</a>", disable_web_page_preview=True)
    await call.message.edit_reply_markup(back_to_customer_menu)
    where_is_msgs.append(we_text)
    where_is_msgs.append(location_text)
    where_is_msgs.append(google_location)

@dp.callback_query_handler(text="contacts")
async def services_menu(call: CallbackQuery):
    await call.message.edit_text("Дастан: +996 707998215")
    await call.message.edit_reply_markup(back_to_customer_menu)

@dp.callback_query_handler(text="leave_contacts")
async def services_menu(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Вы можете здесь оставить ваши контакты, и мы обязательно свяжемся с вами")
    await call.message.edit_reply_markup(back_to_customer_menu)
    await state.set_state("contact")

@dp.message_handler(state="contact")
async def get_contact(message: types.Message, state: FSMContext):
    number = message.text
    await message.delete()
    await message.answer("Спасибо, мы с вами свяжемся")
    await dp.bot.send_message(GROUP, f"Имя: {message.from_user.full_name} \n"
                              f"Номер: {number}")
    await state.finish()