import telebot
from animal import *

from mytoken import MY_TOKEN
"""
    Create 'mytoken.py' with your HTTP API access token, e.g.:
        MY_TOKEN = 'PLACE_YOUR_TOKEN_HERE'
"""


bot = telebot.AsyncTeleBot(MY_TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row(*AnimatedAnimal.ANIMAL_DICT)
bot.infinity_polling(True)
