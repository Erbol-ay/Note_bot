from aiogram import executor

from data.config import ADMINS
from loader import dp, db
import middlewares, filters, handlers
from utils.db_api.test import test
from utils.misc.get_KG_time import get_KG_time
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()

    await on_startup_notify(dispatcher)
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
