from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.menu import inline_choose_menu
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Привет, {message.from_user.full_name}! \n"
                         "Подскажите нам, кто вы?",
                         reply_markup=inline_choose_menu)
    await state.finish()
