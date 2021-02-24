from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("Get_id"))
async def get_id(message: types.Message, state: FSMContext):
    await message.answer("Переотправьте сообщение из чата, чтобы узнать id")
    await state.set_state("getting_id")

@dp.message_handler(state="getting_id")
async def show_id(message: types.Message, state: FSMContext):
    # id = message.forward_from.
    chat_id = message.forward_from.id
    await message.answer(f"id {0}\n"
                         f"chat id {chat_id}")
    await state.finish()