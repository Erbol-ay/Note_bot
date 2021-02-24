from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
PG_USER = env.str("PG_USER")
PG_PASSWORD = env.str("PG_PASSWORD")
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов

IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
DATABASE = env("DATABASE")

GROUP = env.str("GROUP")