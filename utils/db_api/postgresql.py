from typing import Union

import asyncpg
from asyncpg.pool import Pool

from data import config

class Database:
    def __init__(self):
        """Создается база данных без подключения в loader"""

        self.pool: Union[Pool, None] = None

    async def create(self):
        """В этой функции создается подключение к базе"""

        pool = await asyncpg.create_pool(
            user=config.PG_USER,  # Пользователь базы (postgres или ваше имя), для которой была создана роль
            password=config.PG_PASSWORD,  # Пароль к пользователю
            host=config.IP,  # Ip адрес базы данных. Если локальный компьютер - localhost, если докер - название сервиса
            database=config.DATABASE  # Название базы данных. По умолчанию - postgres, если вы не создавали свою
        )
        self.pool = pool


    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id INT NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Fine INT,
        Charge INT,
        Was_noted BOOL,
        Day INT,
        PRIMARY KEY (id))
        """
        await self.pool.execute(sql)

    async def create_table_data(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Data (
        id INT NOT NULL,
        Latitude FLOAT,
        Longitude FLOAT,
        Start_time INT,
        Allowed_time INT,
        Charge INT,
        Fine INT,
        Increased_fine INT,
        Password VARCHAR(255),
        PRIMARY KEY (id)
        )
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, paramteres: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(paramteres, start=1)
        ])
        return sql, tuple(paramteres.values())

    async def add_user(self, id: int, name: str, fine: int = 0, charge: int = 0, was_noted: bool = False, day: int = 0):
        sql = "INSERT INTO Users(id, name, fine, charge, was_noted, day) VALUES ($1, $2, $3, $4, $5, $6)"
        await self.pool.execute(sql, id, name, fine, charge, was_noted, day)

    async def set_data(self, id: int, latitude: float = 0, longitude: float = 0, start_time: int = 0, allowed_time: int = 0,
                       charge: int = 0, fine: int = 0, increased_fine: int = 0, password: str = None):
        sql = "INSERT INTO Data(id, latitude, longitude, start_time, allowed_time, charge, fine, increased_fine, password) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)"
        await self.pool.execute(sql, id, latitude, longitude, start_time, allowed_time, charge, fine, increased_fine, password)

    async def select_data(self, **kwargs):
        sql = "SELECT * FROM Data WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.pool.fetch(sql)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    ###########################
    # Data table updates Begin
    ###########################

    async def update_data_password(self, password, id):
        sql = "UPDATE Data SET password = $1 WHERE id = $2"
        return await self.pool.execute(sql, password, id)

    async def update_data_gps(self, latitude, longitude, id):
        sql = "UPDATE Data SET latitude = $1, longitude = $2 WHERE id = $3"
        return await self.pool.execute(sql, latitude, longitude, id)

    async def update_data_start_time(self, start_time, id):
        sql = "UPDATE Data SET start_time = $1 WHERE id = $2"
        return await self.pool.execute(sql, start_time, id)

    async def update_data_allowed_time(self, allowed_time, id):
        sql = "UPDATE Data SET allowed_time = $1 WHERE id = $2"
        return await self.pool.execute(sql, allowed_time, id)

    async def update_data_fine(self, fine, id):
        sql = "UPDATE Data SET fine = $1 WHERE id = $2"
        return await self.pool.execute(sql, fine, id)

    async def update_data_increased_fine(self, increased_fine, id):
        sql = "UPDATE Data SET increased_fine = $1 WHERE id = $2"
        return await self.pool.execute(sql, increased_fine, id)

    async def update_data_charge(self, charge, id):
        sql = "UPDATE Data SET charge = $1 WHERE id = $2"
        return await self.pool.execute(sql, charge, id)

    #########################
    # Data table updates End
    #########################

    ############################
    # Users table updates Begin
    ############################

    async def update_user_fine(self, fine, charge, id):
        sql = "UPDATE Users SET fine = $1, charge = $2 WHERE id = $3"
        return await self.pool.execute(sql, fine, charge, id)

    async def update_user_was_noted(self, was_noted, id):
        sql = "UPDATE Users SET was_noted = $1 WHERE id = $2"
        return await self.pool.execute(sql, was_noted, id)

    async def update_user_day(self, day, id):
        sql = "UPDATE Users SET day = $1 WHERE id = $2"
        return await self.pool.execute(sql, day, id)

    async def restore_employee_data(self, fine, day):
        sql = "UPDATE Users SET fine = $1, day = $2 WHERE True"
        return await self.pool.execute(sql, fine, day)

    ############################
    # Users table updates END
    ############################

    async def count_users(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM Users")

    async def delete_data(self):
        await self.pool.execute("DELETE FROM Data WHERE True")

    async def delete_user(self, id):
        sql = "DELETE FROM Users WHERE id = $1"
        await self.pool.execute(sql, id)

    async def delete_users(self):
        await self.pool.execute("DELETE FROM Users WHERE True")

    async def delete_table_users(self):
        await self.pool.execute("DROP TABLE Users")