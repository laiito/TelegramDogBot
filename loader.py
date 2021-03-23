import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup
from environs import Env
from animals import ANIMAL_DICT

env = Env()
env.read_env()
MY_TOKEN = env.str("MY_TOKEN")

loop = asyncio.get_event_loop()
bot = Bot(token=MY_TOKEN)
dp = Dispatcher(bot, loop=loop)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(*ANIMAL_DICT)
