import asyncio
from loader import db

async def test():
    await db.delete_users()

    # print("Создаем таблицу Пользователей...")
    # await db.create_table_users()
    # print("Готово")
    # print(" ")
    # print("Добавляем пользователей")
    #
    # await db.add_user(1, "One")
    # await db.add_user(2, "Two")
    # await db.add_user(3, "Three")
    # print("Готово")
    #
    # users = await db.select_all_users()
    # print(f"Получил всех пользователей {users}")
    #
    # user = await db.select_user(id=2)
    # print(f"Получил пользователя: {user}")
