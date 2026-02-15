from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = str(env('BOT_TOKEN'))
WEATHER_API_KEY = str(env('WEATHER_API_KEY'))
DB_USER = str(env('DB_USER'))
DB_PASSWORD = str(env('DB_PASSWORD'))
DB_HOST = str(env('DB_HOST'))
DB_NAME = str(env('DB_NAME'))
DB_PORT = int(env('DB_PORT'))
ADMINS = [int(x) for x in env('ADMINS').split(',')]
